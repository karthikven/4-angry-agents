def get_system_prompt():
    """The foundational instruction for the LLM agent."""
    return """
        You are a member of an investment committee.
        Your goal is to collaborate with your peers to make the best possible investment decision.
        You must think step-by-step, record your thoughts, and then communicate your decision and reasoning clearly.
        Your vote must be one of 'A', 'B', or 'Undecided'.
    """

def get_main_prompt(
    agent_name,
    agent_traits,
    decision_problem,
    other_agent_names,
    full_history,
    scratchpad_content
):
    """The main prompt template for each agent's turn."""
    
    # Format the agent's traits into a readable string
    traits_str = ", ".join([f"{k.replace('_', ' ')}: {v}" for k, v in agent_traits.items()])
    
    return f"""
    Your name is {agent_name}.
    Your personality traits are: {traits_str}.
    The other committee members are: {", ".join(other_agent_names)}.

    ## Investment Problem
    {decision_problem}

    ## History of Deliberation & Voting
    {full_history}

    ## Your Private Scratchpad
    This is for your eyes only. Use it to organize your thoughts before speaking.
    {scratchpad_content}
    ---
    ## Your Task
    It is now your turn.

    1.  **Think**: Review the problem, your personality, and the history. Formulate your thoughts, reasoning deeply about the problem, how you feel about it and other committee members, what your thoughts have been, how they have evolved, patterns you notice, and more, in your scratchpad. Append your new thoughts below the existing thoughts in your scratchpad.
    2.  **Speak**: Based on your thoughts, compose a brief statement to the committee.
    3.  **Vote**: Cast your vote for Option A, Option B, or remain Undecided.

    Provide your response in the requested structured format.
    """

def get_listener_prompt(
    agent_name,
    agent_traits,
    decision_problem,
    full_history,
    speaker_name,
    speaker_speech,
    scratchpad_content
):
    """The prompt for agents who are listening and reacting in a round."""
    
    traits_str = ", ".join([f"{k.replace('_', ' ')}: {v}" for k, v in agent_traits.items()])
    
    return f"""
    Your name is {agent_name}.
    Your personality traits are: {traits_str}.

    ## Investment Problem
    {decision_problem}

    ## History of Deliberation & Voting
    {full_history}

    ## This Round's Speech
    **{speaker_name} just said**: "{speaker_speech}"

    ## Your Private Scratchpad
    {scratchpad_content}
    ---
    ## Your Task
    You are a listener in this round. Based on all the information available to you:

    1.  **Think**: Add your thoughts and notes to your scratchpad.
    2.  **Vote**: Re-evaluate your position and cast your vote for Option A, Option B, or remain Undecided.

    Provide your response in the requested structured format.
    """