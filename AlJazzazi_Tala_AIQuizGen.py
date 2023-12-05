from langchain import PromptTemplate  # Generating prompts
from langchain.chains import LLMChain  # Chain for language model interaction
import streamlit as st  # Creating a web-based interface
from langchain.chat_models import ChatOpenAI  # Chat-based interactions

# Create a quiz prompt template
def createQuizPromptTemplate():
  # String template for the quiz, with placeholders for variables
  quiz_template= """Act as quiz maker, and create a quiz with {questions_num} multiple-choice questions about {quiz_topic}"""
  # Create a prompt
  prompt=PromptTemplate.from_template(quiz_template)
  # Replacing placeholders with specific values
  prompt.format(questions_num=2, quiz_topic="Vincent van Gogh")
  return prompt

# Create Quiz Chain
def quiz_chain(prompt_template, openai_model):
    # Create LLMChain instance
    return LLMChain(llm=openai_model, prompt=prompt_template)

# Main Function
def main():
  # Web Title
  st.title("AI Powered Quiz Generator") 
  # Breif description 
  st.write("Gernerate Quiz based on given topic :)")
  # Create a prompt template
  prompt_template=createQuizPromptTemplate()
  # OpenAI chat model using an API key
  openai_model = ChatOpenAI(openai_api_key="Enter Your API Key Here")
  # Create a quiz chain
  chain=quiz_chain(prompt_template, openai_model)
  # Quiz Topic
  quiz_topic=st.text_area("You want to gerenate quiz about what? ")
  # Questions Number
  questions_num= st.number_input("How many questions do you want? ", min_value=2, max_value=100)
  # Check if the "Generate Now" button is clicked
  if st.button("Generate Now"):
        # Generate the quiz 
        response = chain.run(questions_num=questions_num, quiz_topic=quiz_topic)
        # Quiz generation is complete
        st.write("Done! Here is the quiz :) ")
        st.write(response)
        # Dictionary to store user answers
        answers = {}
        # Iterate through each question 
        for i in range(1, questions_num + 1):
            answer = st.multiselect(f"Question {i} Answer:", response['question_' + str(i)]['answers'])
            answers['Question ' + str(i)] = answer
        # Submitbutton is clicked?
        if st.button("Submit"):
            # Get the correct answers from the generated quiz response
            correct_answers = response['correct_answers']
            # Track of the user's score
            score = 0
            # Display result
            st.write("Quiz Result:")
            # Compare user answers with correct answers
            for i in range(1, questions_num + 1):
                st.write(f"Question {i}: Your Answer - {answers['Question ' + str(i)]}, Correct Answer - {correct_answers['Question ' + str(i)]}")
                if set(answers['Question ' + str(i)]) == set(correct_answers['Question ' + str(i)]):
                    score += 1
            # User's final score
            st.write(f"Your Score: {score}/{questions_num}")
if __name__ == "__main__":
    main()
# To run the code write this command: .\venv\Scripts\activate then streamlit run AlJazzazi_Tala_AIQuizGen.py