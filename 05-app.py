import streamlit as st
import random
import re
from typing import List, Dict, Tuple

class QuizGenerator:
    def __init__(self):
        self.assignment_templates = [
            "Analyze the main themes in the following content: {}",
            "Discuss the key concepts and their relationships in: {}",
            "Evaluate the arguments presented in: {}",
            "Compare and contrast different viewpoints on: {}",
            "Explain the significance and implications of: {}",
            "Critically examine the evidence presented for: {}",
            "Describe the process or methodology outlined in: {}",
            "Assess the strengths and weaknesses of: {}"
        ]
        
        self.question_starters = [
            "What is the main",
            "Which of the following",
            "According to the text",
            "The primary purpose",
            "What does the author",
            "Which statement best",
            "The text suggests that",
            "What can be inferred"
        ]
        
    def extract_key_terms(self, text: str) -> List[str]:
        """Extract key terms from the text using simple heuristics."""
        # Remove common stopwords
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                    'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                    'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'}
        
        # Extract words (remove punctuation and convert to lowercase)
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        
        # Filter out stopwords and short words
        key_terms = [word for word in words if word not in stopwords and len(word) > 3]
        
        # Get unique terms and their frequency
        term_freq = {}
        for term in key_terms:
            term_freq[term] = term_freq.get(term, 0) + 1
        
        # Sort by frequency and return top terms
        sorted_terms = sorted(term_freq.items(), key=lambda x: x[1], reverse=True)
        return [term for term, freq in sorted_terms[:10]]
    
    def extract_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if len(s.strip()) > 10]
    
    def generate_assignments(self, text: str, topic: str = None) -> List[str]:
        """Generate assignment questions based on the input text."""
        assignments = []
        
        # Use topic if provided, otherwise extract from text
        subject = topic if topic else self.extract_main_subject(text)
        
        # Select random templates and generate assignments
        selected_templates = random.sample(self.assignment_templates, 2)
        
        for template in selected_templates:
            assignment = template.format(subject)
            assignments.append(assignment)
        
        return assignments
    
    def extract_main_subject(self, text: str) -> str:
        """Extract the main subject/topic from the text."""
        key_terms = self.extract_key_terms(text)
        if key_terms:
            return f"the concept of {key_terms[0]}"
        else:
            return "the given content"
    
    def generate_quiz_questions(self, text: str) -> List[Dict]:
        """Generate multiple choice questions from the text."""
        sentences = self.extract_sentences(text)
        key_terms = self.extract_key_terms(text)
        
        questions = []
        
        # Generate questions based on available content
        for i in range(3):
            question_data = self.create_question(sentences, key_terms, i)
            questions.append(question_data)
        
        return questions
    
    def create_question(self, sentences: List[str], key_terms: List[str], question_num: int) -> Dict:
        """Create a single multiple choice question."""
        question_types = [
            self.create_definition_question,
            self.create_comprehension_question,
            self.create_inference_question
        ]
        
        # Use different question types
        question_type = question_types[question_num % len(question_types)]
        return question_type(sentences, key_terms)
    
    def create_definition_question(self, sentences: List[str], key_terms: List[str]) -> Dict:
        """Create a definition-based question."""
        if not key_terms:
            return self.create_fallback_question(sentences)
        
        term = random.choice(key_terms[:5])  # Use top 5 terms
        
        question = f"What is the main focus regarding '{term}' in the text?"
        
        # Generate plausible options
        correct_answer = f"The text discusses {term} in the context provided"
        options = [
            correct_answer,
            f"{term} is completely unrelated to the main topic",
            f"{term} is mentioned only in passing without significance",
            f"The text contradicts common understanding of {term}"
        ]
        
        random.shuffle(options)
        correct_index = options.index(correct_answer)
        
        return {
            'question': question,
            'options': options,
            'correct_answer': correct_index,
            'explanation': f"The correct answer focuses on how {term} relates to the main content."
        }
    
    def create_comprehension_question(self, sentences: List[str], key_terms: List[str]) -> Dict:
        """Create a comprehension-based question."""
        if not sentences:
            return self.create_fallback_question(sentences)
        
        sentence = random.choice(sentences[:3])  # Use first few sentences
        
        question = f"According to the text, which statement is most accurate?"
        
        # Create options based on the sentence
        correct_answer = f"The text mentions: {sentence[:50]}..."
        options = [
            correct_answer,
            "The text primarily focuses on historical events",
            "The content is mainly theoretical without practical application",
            "The text contradicts established principles in the field"
        ]
        
        random.shuffle(options)
        correct_index = options.index(correct_answer)
        
        return {
            'question': question,
            'options': options,
            'correct_answer': correct_index,
            'explanation': "This option best reflects the content mentioned in the text."
        }
    
    def create_inference_question(self, sentences: List[str], key_terms: List[str]) -> Dict:
        """Create an inference-based question."""
        question = "What can be inferred from the overall content?"
        
        options = [
            "The content provides informative material on the topic",
            "The text is purely fictional with no factual basis",
            "The content contradicts all established knowledge",
            "The text is primarily focused on entertainment"
        ]
        
        return {
            'question': question,
            'options': options,
            'correct_answer': 0,
            'explanation': "This inference is most reasonable based on the informative nature of the content."
        }
    
    def create_fallback_question(self, sentences: List[str]) -> Dict:
        """Create a basic question when content is limited."""
        question = "What is the primary characteristic of the provided text?"
        
        options = [
            "It contains informative content",
            "It is completely empty",
            "It consists only of numbers",
            "It is written in a foreign language"
        ]
        
        return {
            'question': question,
            'options': options,
            'correct_answer': 0,
            'explanation': "The text provides information that can be analyzed."
        }

def main():
    st.set_page_config(
        page_title="Assignment & Quiz Generator",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 Assignment & Quiz Generator")
    st.markdown("Generate assignments and quiz questions from any text or topic!")
    
    # Sidebar for instructions
    with st.sidebar:
        st.header("📋 Instructions")
        st.markdown("""
        1. **Enter your content** in the text area
        2. **Optionally specify a topic** for more focused questions
        3. **Click Generate** to create assignments and quiz questions
        4. **Review and use** the generated content
        """)
        
        st.header("✨ Features")
        st.markdown("""
        - 2 Essay assignment prompts
        - 3 Multiple choice questions
        - Automatic key term extraction
        - Topic-focused generation
        - Instant results
        """)
    
    # Main input area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Input Content")
        input_text = st.text_area(
            "Enter your document text or content:",
            height=200,
            placeholder="Paste your text here... For example: 'Artificial Intelligence is a branch of computer science that aims to create intelligent machines. It involves machine learning, natural language processing, and computer vision...'"
        )
        
    with col2:
        st.header("🎯 Optional Topic")
        topic = st.text_input(
            "Specific topic (optional):",
            placeholder="e.g., Machine Learning, History, Biology"
        )
        
        st.header("⚙️ Settings")
        difficulty = st.selectbox("Question Difficulty:", ["Mixed", "Basic", "Intermediate", "Advanced"])
    
    # Generate button
    if st.button("🚀 Generate Assignments & Quiz", type="primary", use_container_width=True):
        if input_text.strip():
            generator = QuizGenerator()
            
            with st.spinner("Generating assignments and quiz questions..."):
                # Generate assignments
                assignments = generator.generate_assignments(input_text, topic)
                
                # Generate quiz questions
                quiz_questions = generator.generate_quiz_questions(input_text)
            
            # Display results
            st.success("✅ Generation complete!")
            
            # Assignments section
            st.header("📄 Assignment Questions")
            for i, assignment in enumerate(assignments, 1):
                st.subheader(f"Assignment {i}")
                st.write(assignment)
                st.markdown("---")
            
            # Quiz section
            st.header("❓ Quiz Questions")
            
            # Option to take quiz interactively
            if st.checkbox("🎮 Take Quiz Interactively"):
                score = 0
                user_answers = []
                
                for i, q in enumerate(quiz_questions):
                    st.subheader(f"Question {i+1}")
                    st.write(q['question'])
                    
                    user_answer = st.radio(
                        f"Select your answer for Question {i+1}:",
                        options=range(len(q['options'])),
                        format_func=lambda x: f"{chr(65+x)}. {quiz_questions[st.session_state.get('current_q', i)]['options'][x]}",
                        key=f"q_{i}"
                    )
                    user_answers.append(user_answer)
                
                if st.button("Submit Quiz"):
                    for i, (user_ans, q) in enumerate(zip(user_answers, quiz_questions)):
                        if user_ans == q['correct_answer']:
                            score += 1
                    
                    st.balloons()
                    st.success(f"🎉 Your Score: {score}/{len(quiz_questions)} ({score/len(quiz_questions)*100:.1f}%)")
            
            else:
                # Display quiz with answers
                for i, q in enumerate(quiz_questions, 1):
                    with st.expander(f"Question {i}: {q['question']}", expanded=True):
                        for j, option in enumerate(q['options']):
                            if j == q['correct_answer']:
                                st.success(f"✅ {chr(65+j)}. {option}")
                            else:
                                st.write(f"{chr(65+j)}. {option}")
                        
                        st.info(f"💡 Explanation: {q['explanation']}")
            
            # Download section
            st.header("💾 Export Options")
            
            # Create downloadable content
            export_content = "# Generated Assignments and Quiz\n\n"
            export_content += "## Assignment Questions\n\n"
            for i, assignment in enumerate(assignments, 1):
                export_content += f"**Assignment {i}:**\n{assignment}\n\n"
            
            export_content += "## Quiz Questions\n\n"
            for i, q in enumerate(quiz_questions, 1):
                export_content += f"**Question {i}:** {q['question']}\n"
                for j, option in enumerate(q['options']):
                    marker = "✅" if j == q['correct_answer'] else "  "
                    export_content += f"{marker} {chr(65+j)}. {option}\n"
                export_content += f"*Explanation: {q['explanation']}*\n\n"
            
            st.download_button(
                label="📄 Download as Text File",
                data=export_content,
                file_name="assignments_and_quiz.txt",
                mime="text/plain"
            )
        
        else:
            st.error("⚠️ Please enter some text content to generate assignments and quiz questions.")
    
    # Example content
    if st.button("📖 Load Example Content"):
        example_text = """
        Artificial Intelligence (AI) is a branch of computer science that aims to create intelligent machines capable of performing tasks that typically require human intelligence. These tasks include learning, reasoning, problem-solving, perception, and language understanding.

        Machine Learning is a subset of AI that focuses on the development of algorithms that can learn and improve from experience without being explicitly programmed. It uses statistical techniques to give computers the ability to learn from data.

        Deep Learning, a subset of machine learning, uses neural networks with multiple layers to model and understand complex patterns in data. This technology has revolutionized fields such as image recognition, natural language processing, and speech recognition.

        The applications of AI are vast and growing, including autonomous vehicles, medical diagnosis, financial trading, virtual assistants, and recommendation systems. As AI continues to advance, it raises important questions about ethics, privacy, and the future of work.
        """
        st.rerun()

if __name__ == "__main__":
    main()