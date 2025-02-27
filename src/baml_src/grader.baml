// Defining a data model.
class AdherenceRubric {
  personality_consistency int
  tone_style int
  knowledge_appropriateness int
  self_consistency int
  emotional_authenticity int
}

template_string ChainOfThought() #"
    Outline some relevant information before you answer.
    Example:
    - ...
    - ...
    ...
    {
      ... // schema
    }
"#


function EvalAdherence(character_description: string, interview: string) -> AdherenceRubric {
  client "openai/gpt-4o-mini"
  prompt #"You are a system that evaluates how well AI-generated interview responses adhere to a character. You will be provided the character description, the interview, and a rubric to grade the interview with. You'll output 1-5 ratings for various facets of the AI's adherence to its character.

# Character Description
```
{{character_description}}
```

# **Rubric for Evaluating Interview Adherence**
This rubric evaluates the LLM's ability to stay in character based on different aspects of adherence. The Adherence metric evaluates how well the AI-generated interview responses align with the intended character persona and Guide for Actors in ProDelphi's simulated interviews. It ensures that the responses remain consistent with the character's background, motivations, tone, and knowledge level. This metric ensures that responses:

 - Stay in-character with their persona, including demographics, job, goals, and frustrations.
 - Exhibit domain expertise (or lack thereof) based on the character's profile.
 - Maintain a cohesive personality, avoiding unrealistic shifts in tone or knowledge.
 - Follow the character description, which sets behavioral expectations for different customer types.


| **Field**               | **Description** | **5 - Excellent** | **4 - Good** | **3 - Fair** | **2 - Weak** | **1 - Poor** |
|-------------------------|----------------|-------------------|--------------|-------------|--------------|--------------|
| **Personality Consistency** | Does the response reflect the character's intended personality, including tone and decision-making approach? | Completely aligned with the expected tone and personality. | Mostly in line but with slight inconsistencies. | Some inconsistencies that make the character less believable. | Frequent deviations from the intended personality. | No adherence to the character's personality; responses feel generic or out of place. |
| **Tone & Linguistic Style** | Is the tone of responses appropriate for the character (e.g., formal, casual, skeptical, enthusiastic)? | Matches expected tone and linguistic style perfectly. | Minor stylistic mismatches but still mostly in character. | Noticeable deviations, but some effort to maintain consistency. | Tone fluctuates significantly or is generic. | Completely off-tone or robotic; feels AI-generated. |
| **Domain Knowledge Appropriateness** | Does the response align with the character's expected level of expertise (e.g., an HR manager should have HR-specific knowledge)? | Fully appropriate level of expertise and terminology. | Mostly appropriate with slight lapses. | Shows some correct knowledge but also inconsistencies. | Contains multiple knowledge mismatches. | Completely inappropriate level of knowledge; lacks realism. |
| **Self-Consistency** | Are responses within the interview logically consistent with each other? | No contradictions; maintains internal coherence. | Mostly consistent with minor logical inconsistencies. | Some inconsistencies that may confuse a human interviewer. | Frequent contradictions within the same conversation. | Responses completely contradict previous statements, making the character unreliable. |
| **Emotional Authenticity** | Does the character react in a way that feels realistic and human? | Responses show clear emotional authenticity, aligning with the character's background. | Mostly realistic, but with occasional awkward phrasing. | Some responses feel mechanical or forced. | Feels artificial, overly generic, or lacks emotional depth. | Completely robotic or unnatural; fails to exhibit human-like responses. |

---

### **Example Calculation**
Imagine the following response from a **skeptical HR manager** when asked about AI in hiring:

> _"Oh, AI for hiring? That's an interesting idea! I love new tech. AI is going to completely replace traditional hiring processes soon, and I can't wait!"_

Scored against the rubric:

| **Field** | **Score** | **Why?** |
|-----------|----------|----------|
| **Personality Consistency** | **2** | The character was meant to be skeptical but sounds overly enthusiastic. |
| **Tone & Linguistic Style** | **3** | Mostly appropriate, but enthusiasm is inconsistent with skepticism. |
| **Domain Knowledge** | **4** | Understands AI hiring but makes a sweeping claim about AI replacing hiring completely. |
| **Self-Consistency** | **3** | Later responses may contradict skepticism expected from this persona. |
| **Emotional Authenticity** | **2** | The excitement feels artificial for a skeptical persona. |

Output:
{
  "personality_consistency": 2, 
  "tone_style": 3, 
  "knowledge_appropriateness": 4, 
  "self_consistency": 3, 
  "emotional_authenticity": 2 
}

---

{{ ChainOfThought() }}

After outlining relevant info, use the rubric to evaluate the interview. Be critical and thorough.

{{ ctx.output_format }}

{{ _.role('user') }}
{{interview}}
  "#
}


test TestName {
  functions [EvalAdherence]
  args {
    character_description #"
      template character description
    "#
    interview #"
      template interview contents
    "#
  }
}
