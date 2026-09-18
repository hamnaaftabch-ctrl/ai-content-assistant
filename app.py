import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="✨",
    layout="wide",
)

st.title("✨ AI Content Assistant")
st.write("Create ready-to-publish social media content with Groq.")


def get_api_key():
    try:
        return st.secrets["GROQ_API_KEY"]
    except (KeyError, FileNotFoundError):
        return None


def generate_content(api_key, content_type, platform, topic, audience, tone):
    client = Groq(api_key=api_key)

    prompt = f"""
You are an expert social media content writer.

Create ONE complete, ready-to-publish {content_type} for {platform}.

Content type: {content_type}
Platform: {platform}
Topic: {topic}
Target audience: {audience}
Tone: {tone}

Requirements:
- Start with an engaging hook.
- Write the complete post, not an outline.
- Match the style and length appropriate for the selected platform.
- Make it natural, useful, and easy to read.
- Include a clear call-to-action when appropriate.
- Write a separate short caption.
- Provide 8-12 relevant hashtags.
- Do not invent statistics, studies, quotes, or specific facts.
- Do not explain your process.

Return ONLY:

HOOK:
[hook]

POST:
[complete post]

CAPTION:
[caption]

HASHTAGS:
#hashtag1 #hashtag2 #hashtag3 ...
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are a professional social media content writer.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.7,
        max_tokens=1800,
    )

    return response.choices[0].message.content.strip()


with st.sidebar:
    st.header("Content Settings")

    content_type = st.selectbox(
        "Content Type",
        [
            "Social Media Post",
            "Educational Post",
            "Promotional Post",
            "Storytelling Post",
            "Announcement",
            "Tips / List Post",
        ],
    )

    platform = st.selectbox(
        "Platform",
        [
            "Instagram",
            "LinkedIn",
            "X (Twitter)",
            "Facebook",
            "TikTok",
            "YouTube Community",
        ],
    )

    audience_option = st.selectbox(
        "Target Audience",
        [
            "Students",
            "Gen Z",
            "Young professionals",
            "Entrepreneurs",
            "Small business owners",
            "Creators",
            "Developers",
            "General audience",
            "Custom",
        ],
    )

    audience = audience_option

    if audience_option == "Custom":
        audience = st.text_input(
            "Describe your audience",
            placeholder="e.g. beginner freelancers",
        )

    tone = st.selectbox(
        "Tone",
        [
            "Friendly",
            "Professional",
            "Casual",
            "Gen Z",
            "Educational",
            "Inspirational",
            "Funny",
            "Persuasive",
            "Storytelling",
        ],
    )


topic = st.text_area(
    "What do you want to post about?",
    placeholder="Example: 5 practical ways university students can use AI for studying",
    height=130,
)


if st.button(
    "✨ Generate Content",
    type="primary",
    use_container_width=True,
):
    api_key = get_api_key()

    if not api_key:
        st.error(
            "GROQ_API_KEY is missing. Add it to Streamlit Secrets."
        )

    elif not topic.strip():
        st.warning("Please enter a topic first.")

    elif audience_option == "Custom" and not audience.strip():
        st.warning("Please describe your target audience.")

    else:
        with st.spinner("Creating your content..."):
            try:
                result = generate_content(
                    api_key=api_key,
                    content_type=content_type,
                    platform=platform,
                    topic=topic.strip(),
                    audience=audience,
                    tone=tone,
                )

                st.subheader("Generated Content")

                st.text_area(
                    "Your content",
                    value=result,
                    height=550,
                    label_visibility="collapsed",
                )

            except Exception as e:
                st.error(f"Something went wrong: {e}")
