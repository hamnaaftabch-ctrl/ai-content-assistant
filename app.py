import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="✨",
    layout="wide",
)

# ---------- Styling ----------
st.markdown(
    """
    <style>
        .main-title {
            font-size: 2.6rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
        }
        .subtitle {
            color: #6b7280;
            margin-bottom: 1.5rem;
        }
        .result-card {
            padding: 1rem 1.2rem;
            border-radius: 12px;
            border: 1px solid rgba(128,128,128,.25);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Helpers ----------
def get_api_key():
    """Read GEMINI_API_KEY from Streamlit secrets or environment."""
    try:
        return st.secrets["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError):
        return None


def generate_content(
    api_key: str,
    audience: str,
    tone: str,
    topic: str,
    platform: str,
    extra_instructions: str,
) -> str:
    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an expert social media content assistant.

Create ONE complete, ready-to-publish social media post using the following brief:

Audience: {audience}
Tone: {tone}
Topic: {topic}
Platform: {platform}
Additional instructions: {extra_instructions or "None"}

Requirements:
1. Write a strong platform-appropriate hook/opening.
2. Create the complete post body. Match the normal style and length of the selected platform.
3. Keep the content useful, natural, engaging, and easy to read.
4. Do not invent statistics, quotes, studies, or specific factual claims unless they are common knowledge.
5. Add a clear call-to-action when appropriate.
6. Add 8-12 relevant hashtags. Do not use spammy or unrelated hashtags.
7. Include a short "Caption" section when the platform benefits from a separate caption.
8. Return ONLY the finished content in the following structure:

HOOK
<text>

POST
<text>

CAPTION
<text>

HASHTAGS
#hashtag1 #hashtag2 ...

Do not add explanations, analysis, or notes outside this structure.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.8,
            max_output_tokens=1800,
        ),
    )

    return response.text.strip()


# ---------- App ----------
st.markdown('<div class="main-title">✨ AI Content Assistant</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Generate platform-ready content with Gemini Flash.</div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Content Brief")

    audience = st.selectbox(
        "Audience",
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

    if audience == "Custom":
        audience = st.text_input("Describe your audience", placeholder="e.g. beginner freelancers")

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

    st.divider()

    st.caption("Your Gemini API key should be stored in Streamlit Secrets as GEMINI_API_KEY.")

topic = st.text_area(
    "What do you want to post about?",
    placeholder="Example: 5 practical ways for university students to use AI for studying",
    height=120,
)

extra_instructions = st.text_area(
    "Optional instructions",
    placeholder="Example: Keep it concise, include a question at the end, and avoid emojis.",
    height=90,
)

generate_clicked = st.button(
    "✨ Generate Content",
    type="primary",
    use_container_width=True,
)

if generate_clicked:
    api_key = get_api_key()

    if not api_key:
        st.error(
            "GEMINI_API_KEY is missing. Add it to Streamlit Secrets before generating content."
        )
    elif not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        with st.spinner("Creating your post..."):
            try:
                result = generate_content(
                    api_key=api_key,
                    audience=audience,
                    tone=tone,
                    topic=topic.strip(),
                    platform=platform,
                    extra_instructions=extra_instructions.strip(),
                )

                st.session_state["generated_content"] = result
                st.success("Content generated successfully!")
            except Exception as exc:
                st.error(f"Could not generate content: {exc}")

if "generated_content" in st.session_state:
    st.subheader("Generated Content")
    st.text_area(
        "Edit or copy your post",
        value=st.session_state["generated_content"],
        height=500,
        label_visibility="collapsed",
    )
