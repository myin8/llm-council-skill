"""3-stage LLM Council orchestration."""

from typing import List, Dict, Any, Tuple, Optional
from .openrouter import query_models_parallel, query_model
from .config import DEFAULT_COUNCIL_MODELS, DEFAULT_CHAIRMAN_MODEL


async def stage1_collect_responses(
    user_query: str,
    models: Optional[List[str]] = None,
    verbose: bool = False
) -> List[Dict[str, Any]]:
    """
    Stage 1: Collect individual responses from all council models.

    Args:
        user_query: The user's question
        models: Optional list of model identifiers (defaults to config)
        verbose: If True, include full raw API responses

    Returns:
        List of dicts with 'model' and 'response' keys (and optionally 'raw_response')
    """
    if models is None:
        models = DEFAULT_COUNCIL_MODELS

    messages = [{"role": "user", "content": user_query}]

    # Query all models in parallel
    responses = await query_models_parallel(models, messages, verbose=verbose)

    # Format results
    stage1_results = []
    for model, response in responses.items():
        if response is not None:  # Only include successful responses
            result = {
                "model": model,
                "response": response.get('content', '')
            }
            if verbose and 'raw_response' in response:
                result['raw_response'] = response['raw_response']
            stage1_results.append(result)

    return stage1_results


async def stage2_collect_rankings(
    user_query: str,
    stage1_results: List[Dict[str, Any]],
    models: Optional[List[str]] = None,
    verbose: bool = False
) -> Tuple[List[Dict[str, Any]], Dict[str, str]]:
    """
    Stage 2: Each model ranks the anonymized responses.

    Args:
        user_query: The original user query
        stage1_results: Results from Stage 1
        models: Optional list of model identifiers (defaults to config)
        verbose: If True, include full raw API responses

    Returns:
        Tuple of (rankings list, label_to_model mapping)
    """
    if models is None:
        models = DEFAULT_COUNCIL_MODELS

    # Create anonymized labels for responses (Response A, Response B, etc.)
    labels = [chr(65 + i) for i in range(len(stage1_results))]  # A, B, C, ...

    # Create mapping from label to model name
    label_to_model = {
        f"Response {label}": result['model']
        for label, result in zip(labels, stage1_results)
    }

    # Build the ranking prompt
    responses_text = "\n\n".join([
        f"Response {label}:\n{result['response']}"
        for label, result in zip(labels, stage1_results)
    ])

    ranking_prompt = f"""You are evaluating different responses to the following question:

Question: {user_query}

Here are the responses from different models (anonymized):

{responses_text}

Your task:
1. First, evaluate each response individually. For each response, explain what it does well and what it does poorly.
2. Then, at the very end of your response, provide a final ranking.

IMPORTANT: Your final ranking MUST be formatted EXACTLY as follows:
- Start with the line "FINAL RANKING:" (all caps, with colon)
- Then list the responses from best to worst as a numbered list
- Each line should be: number, period, space, then ONLY the response label (e.g., "1. Response A")
- Do not add any other text or explanations in the ranking section

Example of the correct format for your ENTIRE response:

Response A provides good detail on X but misses Y...
Response B is accurate but lacks depth on Z...
Response C offers the most comprehensive answer...

FINAL RANKING:
1. Response C
2. Response A
3. Response B

Now provide your evaluation and ranking:"""

    messages = [{"role": "user", "content": ranking_prompt}]

    # Get rankings from all council models in parallel
    responses = await query_models_parallel(models, messages, verbose=verbose)

    # Format results
    stage2_results = []
    for model, response in responses.items():
        if response is not None:
            full_text = response.get('content', '')
            parsed = parse_ranking_from_text(full_text)
            result = {
                "model": model,
                "evaluation": full_text,
                "parsed_ranking": parsed
            }
            if verbose and 'raw_response' in response:
                result['raw_response'] = response['raw_response']
            stage2_results.append(result)

    return stage2_results, label_to_model


async def stage3_synthesize_final(
    user_query: str,
    stage1_results: List[Dict[str, Any]],
    stage2_results: List[Dict[str, Any]],
    chairman_model: Optional[str] = None,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Stage 3: Chairman synthesizes final response.

    Args:
        user_query: The original user query
        stage1_results: Individual model responses from Stage 1
        stage2_results: Rankings from Stage 2
        chairman_model: Optional chairman model (defaults to config)
        verbose: If True, include full raw API response

    Returns:
        Dict with 'model' and 'synthesis' keys (and optionally 'raw_response')
    """
    if chairman_model is None:
        chairman_model = DEFAULT_CHAIRMAN_MODEL

    # Build comprehensive context for chairman
    stage1_text = "\n\n".join([
        f"Model: {result['model']}\nResponse: {result['response']}"
        for result in stage1_results
    ])

    stage2_text = "\n\n".join([
        f"Model: {result['model']}\nEvaluation: {result['evaluation']}"
        for result in stage2_results
    ])

    chairman_prompt = f"""You are the Chairman of an LLM Council. Multiple AI models have provided responses to a user's question, and then ranked each other's responses.

Original Question: {user_query}

STAGE 1 - Individual Responses:
{stage1_text}

STAGE 2 - Peer Rankings:
{stage2_text}

Your task as Chairman is to synthesize all of this information into a single, comprehensive, accurate answer to the user's original question. Consider:
- The individual responses and their insights
- The peer rankings and what they reveal about response quality
- Any patterns of agreement or disagreement

Provide a clear, well-reasoned final answer that represents the council's collective wisdom:"""

    messages = [{"role": "user", "content": chairman_prompt}]

    # Query the chairman model
    response = await query_model(chairman_model, messages, verbose=verbose)

    if response is None:
        # Fallback if chairman fails
        return {
            "model": chairman_model,
            "synthesis": "Error: Unable to generate final synthesis."
        }

    result = {
        "model": chairman_model,
        "synthesis": response.get('content', '')
    }

    if verbose and 'raw_response' in response:
        result['raw_response'] = response['raw_response']

    return result


def parse_ranking_from_text(ranking_text: str) -> List[str]:
    """
    Parse the FINAL RANKING section from the model's response.

    Args:
        ranking_text: The full text response from the model

    Returns:
        List of response labels in ranked order
    """
    import re

    # Look for "FINAL RANKING:" section
    if "FINAL RANKING:" in ranking_text:
        # Extract everything after "FINAL RANKING:"
        parts = ranking_text.split("FINAL RANKING:")
        if len(parts) >= 2:
            ranking_section = parts[1]
            # Try to extract numbered list format (e.g., "1. Response A")
            # This pattern looks for: number, period, optional space, "Response X"
            numbered_matches = re.findall(r'\d+\.\s*Response [A-Z]', ranking_section)
            if numbered_matches:
                # Extract just the "Response X" part
                return [re.search(r'Response [A-Z]', m).group() for m in numbered_matches]

            # Fallback: Extract all "Response X" patterns in order
            matches = re.findall(r'Response [A-Z]', ranking_section)
            return matches

    # Fallback: try to find any "Response X" patterns in order
    matches = re.findall(r'Response [A-Z]', ranking_text)
    return matches


def calculate_aggregate_rankings(
    stage2_results: List[Dict[str, Any]],
    label_to_model: Dict[str, str]
) -> List[Dict[str, Any]]:
    """
    Calculate aggregate rankings across all models.

    Args:
        stage2_results: Rankings from each model
        label_to_model: Mapping from anonymous labels to model names

    Returns:
        List of dicts with model name and average rank, sorted best to worst
    """
    from collections import defaultdict

    # Track positions for each model
    model_positions = defaultdict(list)

    for ranking in stage2_results:
        evaluation_text = ranking['evaluation']

        # Parse the ranking from the structured format
        parsed_ranking = parse_ranking_from_text(evaluation_text)

        for position, label in enumerate(parsed_ranking, start=1):
            if label in label_to_model:
                model_name = label_to_model[label]
                model_positions[model_name].append(position)

    # Calculate average position for each model
    aggregate = []
    for model, positions in model_positions.items():
        if positions:
            avg_rank = sum(positions) / len(positions)
            aggregate.append({
                "model": model,
                "average_rank": round(avg_rank, 2),
                "rankings_count": len(positions)
            })

    # Sort by average rank (lower is better)
    aggregate.sort(key=lambda x: x['average_rank'])

    return aggregate


async def run_full_council(
    user_query: str,
    models: Optional[List[str]] = None,
    chairman_model: Optional[str] = None,
    max_stages: int = 3,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Run the complete 3-stage council process.

    Args:
        user_query: The user's question
        models: Optional list of council model identifiers
        chairman_model: Optional chairman model identifier
        max_stages: Maximum stage to run (1, 2, or 3)
        verbose: If True, include full raw API responses with metadata

    Returns:
        Dict with query, models, chairman_model, and stage results
    """
    if models is None:
        models = DEFAULT_COUNCIL_MODELS
    if chairman_model is None:
        chairman_model = DEFAULT_CHAIRMAN_MODEL

    result = {
        "query": user_query,
        "models": models,
        "chairman_model": chairman_model,
    }

    # Stage 1: Collect individual responses
    stage1_results = await stage1_collect_responses(user_query, models, verbose=verbose)

    if not stage1_results:
        result["error"] = "All models failed to respond. Please try again."
        return result

    result["stage1"] = stage1_results

    if max_stages < 2:
        return result

    # Stage 2: Collect rankings
    stage2_results, label_to_model = await stage2_collect_rankings(
        user_query, stage1_results, models, verbose=verbose
    )

    # Calculate aggregate rankings
    aggregate_rankings = calculate_aggregate_rankings(stage2_results, label_to_model)

    result["stage2"] = {
        "evaluations": stage2_results,
        "label_to_model": label_to_model,
        "aggregate_rankings": aggregate_rankings
    }

    if max_stages < 3:
        return result

    # Stage 3: Synthesize final answer
    stage3_result = await stage3_synthesize_final(
        user_query,
        stage1_results,
        stage2_results,
        chairman_model,
        verbose=verbose
    )

    result["stage3"] = stage3_result

    return result
