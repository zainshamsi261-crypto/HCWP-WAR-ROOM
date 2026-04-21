import streamlit as st
import google.generativeai as genai
import PIL.Image
import io

# 1. Page Config & Branding for HC•WP
st.set_page_config(page_title="HC•WP Alliance Hub", page_icon="⚔️", layout="wide")
st.title("⚔️ HC•WP Alliance Command Center")
st.markdown(f"**Commander ZainShams**, welcome to the alliance hub.")

# 2. Sidebar Setup (Simplified)
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    
    # We need the Pro model for good image generation
    model_choice = "gemini-2.5-pro" 
    st.caption(f"Using Model: {model_choice}")
    st.markdown("---")
    st.info("This tool requires an API key with Imagen 3 access enabled.")

# 3. Handle Navigation using Tabs
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_choice)

    # Create two distinct tabs
    tab1, tab2 = st.tabs(["⚔️ War Advisor", "📢 Recruitment Poster"])

    # ==========================================
    # Tab 1: War Advisor (The previous script)
    # ==========================================
    with tab1:
        st.header("Alliance War Strategic Advisor")
        boss = st.text_input("Which Boss are we facing?", placeholder="e.g. Maestro, Hulkling")
        nodes = st.text_area("List the active nodes", placeholder="e.g. Glancing, Buffet, Thorns")

        if st.button("Get Strategy", key="war_btn"):
            if boss and nodes:
                with st.spinner("Analyzing counters..."):
                    prompt = f"""
                    You are a strategic advisor for a high-level MCOC alliance 'HC•WP'.
                    Provide a detailed strategy for {boss} on these nodes: {nodes}.
                    Include Top 3 Champions, recommended playstyle, and key synergies.
                    """
                    response = model.generate_content(prompt)
                    st.success("Strategy Found!")
                    st.markdown(response.text)
            else:
                st.warning("Please fill in both the Boss and Nodes fields.")

    # ==========================================
    # Tab 2: Recruitment Poster (NEW!)
    # ==========================================
    with tab2:
        st.header("Create a Custom Recruitment Poster")
        st.markdown("Generate a stylized poster to attract new high-level active players to **HC•WP**.")

        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("Poster Details")
            hero_focus = st.text_input("Main Hero Focus", value="Captain America (Sam Wilson)")
            style_override = st.selectbox("Poster Style", 
                                          ["Classic Marvel Comic", "Dark/Gritty Cinematic", "Modern Digital Art"])
            alliance_vibe = st.text_area("Alliance Vibe/Requirements", 
                                         value="Focus on High Tier War, Active Daily, Friendly but Competitive.")
            
            # We add a hidden requirement for the alliance tag
            custom_prompt_suffix = "The text 'JOIN HC•WP' must be clearly integrated into the design."

            generate_image_btn = st.button("Generate Poster Design")

        with col2:
            if generate_image_btn:
                if hero_focus:
                    with st.spinner(f"Designing your {hero_focus} poster... this may take 20 seconds."):
                        
                        # We construct the image prompt
                        image_prompt = f"""
                        A dynamic, action-oriented MCOC-style recruitment poster featuring {hero_focus}. 
                        The style is {style_override}. The image must look intense and professional, 
                        fit for a top-tier alliance advertisement. {alliance_vibe}. 
                        The text 'JOIN HC•WP' is subtly yet clearly integrated into the scene's architecture or energy effects.
                        """
                        
                        # Generate the image using Gemini (calls Imagen 3)
                        generated_image = model.generate_content(image_prompt)

                        # Check if generation worked and display the result
                        if generated_image.images:
                            image_data = generated_image.images[0]
                            
                            # Convert to PIL Image for Streamlit
                            img = PIL.Image.open(io.BytesIO(image_data._raw_bytes))
                            st.image(img, caption=f"HC•WP Recruitment: {hero_focus}", use_column_width=True)
                            
                            # Add a download button
                            st.download_button(
                                label="Download Poster",
                                data=image_data._raw_bytes,
                                file_name=f"HCWP_{hero_focus.replace(' ', '_')}_Recruitment.png",
                                mime="image/png"
                            )
                        else:
                            st.error("Image generation failed. This might be due to a strict safety filter or API limitations.")
                else:
                    st.warning("Please specify a Main Hero Focus.")

else:
    st.warning("🔑 Please enter your Gemini API key in the sidebar to access the Command Center.")
    st.info("You can get a free API key at: [Google AI Studio](https://aistudio.google.com/)")
