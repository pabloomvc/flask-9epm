in this folder you'll find the following.

Folders: 
- personas: Prompts describing each one of the personas. One of them is the tutor. And there could potentially be others.
- situation_prompts: Prompts describing each one of the situations/roleplay scenarios.
- tutor_prompts: This is for [AskVersa]. Contains each one of the things you can ask the tutor.
- word_by_word: Contains the prompts to get the word by word translations of a message.

Files: 
- get_corrections_prompt: The prompts that gets the errors and corrections of a message.
- initial_prompt: Base prompt. Includes the fundamental instructions. Other prompts are added to this one.
- message_instructions: Contains the format instructions for the response. Specifies that the response should be in JSON format with specific keys.

How does this work?
- The system prompt consists of: 
	- a persona (from the personas folder)
	- the base instructions (initial_prompt)
	- a situation (from the situation_prompts)
- The message instructions are added to the end of the last message in the conversation.
