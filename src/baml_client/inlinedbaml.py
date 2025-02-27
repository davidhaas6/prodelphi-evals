###############################################################################
#
#  Welcome to Baml! To use this generated code, please run the following:
#
#  $ pip install baml-py
#
###############################################################################

# This file was generated by BAML: please do not edit it. Instead, edit the
# BAML files and re-generate this code.
#
# ruff: noqa: E501,F401
# flake8: noqa: E501,F401
# pylint: disable=unused-import,line-too-long
# fmt: off

file_map = {
    
    "clients.baml": "// Learn more about clients at https://docs.boundaryml.com/docs/snippets/clients/overview\n\nclient<llm> CustomGPT4o {\n  provider openai\n  options {\n    model \"gpt-4o\"\n    api_key env.OPENAI_API_KEY\n  }\n}\n\nclient<llm> CustomGPT4oMini {\n  provider openai\n  retry_policy Exponential\n  options {\n    model \"gpt-4o-mini\"\n    api_key env.OPENAI_API_KEY\n  }\n}\n\nclient<llm> CustomSonnet {\n  provider anthropic\n  options {\n    model \"claude-3-5-sonnet-20241022\"\n    api_key env.ANTHROPIC_API_KEY\n  }\n}\n\n\nclient<llm> CustomHaiku {\n  provider anthropic\n  retry_policy Constant\n  options {\n    model \"claude-3-haiku-20240307\"\n    api_key env.ANTHROPIC_API_KEY\n  }\n}\n\n// https://docs.boundaryml.com/docs/snippets/clients/round-robin\nclient<llm> CustomFast {\n  provider round-robin\n  options {\n    // This will alternate between the two clients\n    strategy [CustomGPT4oMini, CustomHaiku]\n  }\n}\n\n// https://docs.boundaryml.com/docs/snippets/clients/fallback\nclient<llm> OpenaiFallback {\n  provider fallback\n  options {\n    // This will try the clients in order until one succeeds\n    strategy [CustomGPT4oMini, CustomGPT4oMini]\n  }\n}\n\n// https://docs.boundaryml.com/docs/snippets/clients/retry\nretry_policy Constant {\n  max_retries 3\n  // Strategy is optional\n  strategy {\n    type constant_delay\n    delay_ms 200\n  }\n}\n\nretry_policy Exponential {\n  max_retries 2\n  // Strategy is optional\n  strategy {\n    type exponential_backoff\n    delay_ms 300\n    multiplier 1.5\n    max_delay_ms 10000\n  }\n}",
    "generators.baml": "// This helps use auto generate libraries you can use in the language of\n// your choice. You can have multiple generators if you use multiple languages.\n// Just ensure that the output_dir is different for each generator.\ngenerator target {\n    // Valid values: \"python/pydantic\", \"typescript\", \"ruby/sorbet\", \"rest/openapi\"\n    output_type \"python/pydantic\"\n\n    // Where the generated code will be saved (relative to baml_src/)\n    output_dir \"../\"\n\n    // The version of the BAML package you have installed (e.g. same version as your baml-py or @boundaryml/baml).\n    // The BAML VSCode extension version should also match this version.\n    version \"0.77.0\"\n\n    // Valid values: \"sync\", \"async\"\n    // This controls what `b.FunctionName()` will be (sync or async).\n    default_client_mode sync\n}\n",
    "grader.baml": "// Defining a data model.\nclass AdherenceRubric {\n  personality_consistency int\n  tone_style int\n  knowledge_appropriateness int\n  self_consistency int\n  emotional_authenticity int\n}\n\ntemplate_string ChainOfThought() #\"\n    Outline some relevant information before you answer.\n    Example:\n    - ...\n    - ...\n    ...\n    {\n      ... // schema\n    }\n\"#\n\n\nfunction EvalAdherence(character_description: string, interview: string) -> AdherenceRubric {\n  client \"openai/gpt-4o-mini\"\n  prompt #\"You are a system that evaluates how well AI-generated interview responses adhere to a character. You will be provided the character description, the interview, and a rubric to grade the interview with. You'll output 1-5 ratings for various facets of the AI's adherence to its character.\n\n# Character Description\n```\n{{character_description}}\n```\n\n# **Rubric for Evaluating Interview Adherence**\nThis rubric evaluates the LLM's ability to stay in character based on different aspects of adherence. The Adherence metric evaluates how well the AI-generated interview responses align with the intended character persona and Guide for Actors in ProDelphi's simulated interviews. It ensures that the responses remain consistent with the character's background, motivations, tone, and knowledge level. This metric ensures that responses:\n\n - Stay in-character with their persona, including demographics, job, goals, and frustrations.\n - Exhibit domain expertise (or lack thereof) based on the character's profile.\n - Maintain a cohesive personality, avoiding unrealistic shifts in tone or knowledge.\n - Follow the character description, which sets behavioral expectations for different customer types.\n\n\n| **Field**               | **Description** | **5 - Excellent** | **4 - Good** | **3 - Fair** | **2 - Weak** | **1 - Poor** |\n|-------------------------|----------------|-------------------|--------------|-------------|--------------|--------------|\n| **Personality Consistency** | Does the response reflect the character's intended personality, including tone and decision-making approach? | Completely aligned with the expected tone and personality. | Mostly in line but with slight inconsistencies. | Some inconsistencies that make the character less believable. | Frequent deviations from the intended personality. | No adherence to the character's personality; responses feel generic or out of place. |\n| **Tone & Linguistic Style** | Is the tone of responses appropriate for the character (e.g., formal, casual, skeptical, enthusiastic)? | Matches expected tone and linguistic style perfectly. | Minor stylistic mismatches but still mostly in character. | Noticeable deviations, but some effort to maintain consistency. | Tone fluctuates significantly or is generic. | Completely off-tone or robotic; feels AI-generated. |\n| **Domain Knowledge Appropriateness** | Does the response align with the character's expected level of expertise (e.g., an HR manager should have HR-specific knowledge)? | Fully appropriate level of expertise and terminology. | Mostly appropriate with slight lapses. | Shows some correct knowledge but also inconsistencies. | Contains multiple knowledge mismatches. | Completely inappropriate level of knowledge; lacks realism. |\n| **Self-Consistency** | Are responses within the interview logically consistent with each other? | No contradictions; maintains internal coherence. | Mostly consistent with minor logical inconsistencies. | Some inconsistencies that may confuse a human interviewer. | Frequent contradictions within the same conversation. | Responses completely contradict previous statements, making the character unreliable. |\n| **Emotional Authenticity** | Does the character react in a way that feels realistic and human? | Responses show clear emotional authenticity, aligning with the character's background. | Mostly realistic, but with occasional awkward phrasing. | Some responses feel mechanical or forced. | Feels artificial, overly generic, or lacks emotional depth. | Completely robotic or unnatural; fails to exhibit human-like responses. |\n\n---\n\n### **Example Calculation**\nImagine the following response from a **skeptical HR manager** when asked about AI in hiring:\n\n> _\"Oh, AI for hiring? That's an interesting idea! I love new tech. AI is going to completely replace traditional hiring processes soon, and I can't wait!\"_\n\nScored against the rubric:\n\n| **Field** | **Score** | **Why?** |\n|-----------|----------|----------|\n| **Personality Consistency** | **2** | The character was meant to be skeptical but sounds overly enthusiastic. |\n| **Tone & Linguistic Style** | **3** | Mostly appropriate, but enthusiasm is inconsistent with skepticism. |\n| **Domain Knowledge** | **4** | Understands AI hiring but makes a sweeping claim about AI replacing hiring completely. |\n| **Self-Consistency** | **3** | Later responses may contradict skepticism expected from this persona. |\n| **Emotional Authenticity** | **2** | The excitement feels artificial for a skeptical persona. |\n\nOutput:\n{\n  \"personality_consistency\": 2, \n  \"tone_style\": 3, \n  \"knowledge_appropriateness\": 4, \n  \"self_consistency\": 3, \n  \"emotional_authenticity\": 2 \n}\n\n---\n\n{{ ChainOfThought() }}\n\nAfter outlining relevant info, use the rubric to evaluate the interview. Be critical and thorough.\n\n{{ ctx.output_format }}\n\n{{ _.role('user') }}\n{{interview}}\n  \"#\n}\n\n\ntest TestName {\n  functions [EvalAdherence]\n  args {\n    character_description #\"\n      template character description\n    \"#\n    interview #\"\n      template interview contents\n    \"#\n  }\n}\n",
    "resume.baml": "// Defining a data model.\nclass Resume {\n  name string\n  email string\n  experience string[]\n  skills string[]\n}\n\n// Create a function to extract the resume from a string.\nfunction ExtractResume(resume: string) -> Resume {\n  // Specify a client as provider/model-name\n  // you can use custom LLM params with a custom client name from clients.baml like \"client CustomHaiku\"\n  client \"openai/gpt-4o\" // Set OPENAI_API_KEY to use this client.\n  prompt #\"\n    Extract from this content:\n    {{ resume }}\n\n    {{ ctx.output_format }}\n  \"#\n}\n\n// Test the function with a sample resume. Open the VSCode playground to run this.\ntest vaibhav_resume {\n  functions [ExtractResume]\n  args {\n    resume #\"\n      Vaibhav Gupta\n      vbv@boundaryml.com\n\n      Experience:\n      - Founder at BoundaryML\n      - CV Engineer at Google\n      - CV Engineer at Microsoft\n\n      Skills:\n      - Rust\n      - C++\n    \"#\n  }\n}\n",
}

def get_baml_files():
    return file_map