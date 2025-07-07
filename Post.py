import streamlit as st
from openai import OpenAI
from typing import Dict, Any
import os

# Set page configuration
st.set_page_config(
    page_title="Social Media Post Generator",
    page_icon="📱",
    layout="wide"
)

def generate_social_media_posts(event_description: str, api_key: str) -> Dict[str, str]:
    """
    Generate social media posts for LinkedIn, Twitter, and WhatsApp
    """
    # Initialize OpenAI client with API key
    client = OpenAI(api_key=api_key)
    
    # Define prompts for each platform
    prompts = {
        "linkedin": f"""
        Create a professional LinkedIn post about the following event: {event_description}
        
        Guidelines:
        - Keep it professional and business-appropriate
        - Use industry-relevant language
        - Include relevant hashtags (2-3 maximum)
        - Focus on insights, learnings, or professional value
        - Keep it under 200 words
        - Use a tone that's informative and engaging for professional network
        """,
        
        "twitter": f"""
        Create a Twitter post about the following event: {event_description}
        
        Guidelines:
        - Keep it under 280 characters
        - Be politically correct and neutral
        - Avoid controversial language
        - Use 1-2 relevant hashtags
        - Make it engaging but respectful
        - Focus on facts and positive aspects
        """,
        
        "whatsapp": f"""
        Create a WhatsApp message about the following event: {event_description}
        
        Guidelines:
        - Keep it friendly and casual
        - Use conversational tone
        - Include emojis where appropriate
        - Make it personal and relatable
        - Keep it concise but warm
        - Write as if messaging a friend
        """
    }
    
    posts = {}
    
    for platform, prompt in prompts.items():
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a social media content creator who specializes in creating platform-specific content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            posts[platform] = response.choices[0].message.content.strip()
            
        except Exception as e:
            posts[platform] = f"Error generating {platform} post: {str(e)}"
    
    return posts

def main():
    st.title("🚀 Social Media Post Generator")
    st.markdown("Generate tailored posts for LinkedIn, Twitter, and WhatsApp from any event description!")
    
    # Sidebar for API key
    with st.sidebar:
        st.header("🔑 Configuration")
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key. Get one at https://platform.openai.com/api-keys",
            placeholder="sk-..."
        )
        
        if api_key:
            st.success("✅ API key entered")
        else:
            st.warning("⚠️ Please enter your OpenAI API key")
        
        st.markdown("---")
        st.markdown("### 📝 Platform Guidelines")
        st.markdown("**LinkedIn:** Professional, business-focused")
        st.markdown("**Twitter:** Politically correct, neutral tone")
        st.markdown("**WhatsApp:** Friendly, casual conversation")
    
    # Main content area
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("📅 Event Details")
        event_description = st.text_area(
            "Describe your event:",
            height=150,
            placeholder="e.g., Our company just launched a new AI-powered mobile app that helps users track their fitness goals with personalized recommendations..."
        )
        
        generate_button = st.button("🎯 Generate Posts", type="primary")
    
    with col2:
        st.header("📱 Generated Posts")
        
        if generate_button:
            if not api_key:
                st.error("Please enter your OpenAI API key in the sidebar.")
            elif not event_description.strip():
                st.error("Please enter an event description.")
            else:
                with st.spinner("Generating posts..."):
                    posts = generate_social_media_posts(event_description, api_key)
                
                # Display posts in tabs
                tab1, tab2, tab3 = st.tabs(["💼 LinkedIn", "🐦 Twitter", "💬 WhatsApp"])
                
                with tab1:
                    st.subheader("LinkedIn Post")
                    st.text_area("", value=posts["linkedin"], height=150, key="linkedin_post")
                    if st.button("📋 Copy LinkedIn Post"):
                        st.success("LinkedIn post copied to clipboard!")
                
                with tab2:
                    st.subheader("Twitter Post")
                    char_count = len(posts["twitter"])
                    color = "green" if char_count <= 280 else "red"
                    st.markdown(f"Character count: <span style='color: {color}'>{char_count}/280</span>", unsafe_allow_html=True)
                    st.text_area("", value=posts["twitter"], height=100, key="twitter_post")
                    if st.button("📋 Copy Twitter Post"):
                        st.success("Twitter post copied to clipboard!")
                
                with tab3:
                    st.subheader("WhatsApp Message")
                    st.text_area("", value=posts["whatsapp"], height=150, key="whatsapp_post")
                    if st.button("📋 Copy WhatsApp Message"):
                        st.success("WhatsApp message copied to clipboard!")
    
    # Footer
    st.markdown("---")
    st.markdown("### 💡 Tips for Better Results")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Be Specific**")
        st.markdown("Include key details about your event, audience, and goals.")
    
    with col2:
        st.markdown("**Context Matters**")
        st.markdown("Mention the type of event, industry, and target audience.")
    
    with col3:
        st.markdown("**Review & Edit**")
        st.markdown("Always review generated content before posting.")

if __name__ == "__main__":
    main()