"""Streamlit GUI for Knitty CV Enhancement."""

import streamlit as st
import asyncio
import sys
from pathlib import Path
import tempfile
import json
from knitty.core.pipeline import EnhancementPipeline
from knitty.config.settings import get_settings

# Page configuration
st.set_page_config(
    page_title="Knitty - Resume Factory",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional design
st.markdown("""
    <style>
        .main-header {
            font-size: 3rem;
            font-weight: 700;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        .sub-header {
            font-size: 1.2rem;
            color: #666;
            text-align: center;
            margin-bottom: 2rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
        }
        .success-box {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 1rem 0;
        }
        .info-box {
            background-color: #d1ecf1;
            border: 1px solid #bee5eb;
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 1rem 0;
        }
        .stProgress > div > div > div {
            background-color: #1f77b4;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "pipeline" not in st.session_state:
    try:
        st.session_state.pipeline = EnhancementPipeline()
        st.session_state.initialized = True
    except Exception as e:
        st.error(f"Failed to initialize pipeline: {e}")
        st.session_state.initialized = False

if "results" not in st.session_state:
    st.session_state.results = None


def run_async(coro):
    """Run async function in Streamlit."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    return loop.run_until_complete(coro)


def main():
    """Main application."""
    # Header
    st.markdown('<h1 class="main-header">🧵 Knitty</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Resume Factory - Intelligent CV Tailoring System</p>',
        unsafe_allow_html=True
    )
    
    if not st.session_state.initialized:
        st.error("❌ Application not initialized. Please check your configuration.")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        st.info("""
        **How it works:**
        1. Upload your CV (PDF)
        2. Provide job posting (URL or text)
        3. Add any additional information
        4. Get your enhanced CV!
        """)
        
        st.markdown("---")
        st.markdown("### 📊 Settings")
        
        show_keywords = st.checkbox("Show extracted keywords", value=False)
        show_metrics = st.checkbox("Show similarity metrics", value=True)
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["📄 Enhance CV", "📊 Results", "ℹ️ About"])
    
    with tab1:
        st.header("CV Enhancement")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📎 Upload CV")
            cv_file = st.file_uploader(
                "Upload your CV (PDF)",
                type=["pdf"],
                help="Upload your CV in PDF format"
            )
            
            st.markdown("---")
            
            st.subheader("📝 Additional Information")
            additional_info = st.text_area(
                "Add any additional information about your experience, skills, or projects",
                height=150,
                help="This will be combined with your CV content"
            )
        
        with col2:
            st.subheader("💼 Job Posting")
            
            input_method = st.radio(
                "Input method",
                ["URL", "Text"],
                help="Choose how to provide the job posting"
            )
            
            job_posting_url = None
            job_posting_text = None
            
            if input_method == "URL":
                job_posting_url = st.text_input(
                    "Job Posting URL",
                    placeholder="https://www.linkedin.com/jobs/view/...",
                    help="Paste the URL of the job posting"
                )
            else:
                job_posting_text = st.text_area(
                    "Job Posting Text",
                    height=200,
                    help="Paste the full job posting text"
                )
        
        st.markdown("---")
        
        # Process button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            process_button = st.button(
                "🚀 Enhance My CV",
                type="primary",
                use_container_width=True
            )
        
        if process_button:
            # Validation
            if not cv_file:
                st.error("❌ Please upload a CV file")
                return
            
            if not job_posting_url and not job_posting_text:
                st.error("❌ Please provide either a job posting URL or text")
                return
            
            # Process
            with st.spinner("🔄 Processing your CV... This may take a minute."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                        tmp_file.write(cv_file.read())
                        tmp_path = tmp_file.name
                    
                    try:
                        status_text.text("📄 Extracting CV content...")
                        progress_bar.progress(10)
                        
                        status_text.text("🌐 Processing job posting...")
                        progress_bar.progress(30)
                        
                        status_text.text("🔍 Extracting keywords...")
                        progress_bar.progress(50)
                        
                        status_text.text("📊 Calculating similarity...")
                        progress_bar.progress(70)
                        
                        status_text.text("✨ Enhancing CV...")
                        progress_bar.progress(90)
                        
                        # Run async pipeline
                        result = run_async(
                            st.session_state.pipeline.process(
                                cv_pdf_path=tmp_path,
                                job_posting_url=job_posting_url if job_posting_url else None,
                                job_posting_text=job_posting_text if job_posting_text else None,
                                additional_info=additional_info if additional_info else None
                            )
                        )
                        
                        progress_bar.progress(100)
                        status_text.text("✅ Complete!")
                        
                        # Store results
                        st.session_state.results = result
                        
                        st.success("🎉 CV enhancement completed successfully!")
                        st.balloons()
                        
                    finally:
                        # Clean up
                        Path(tmp_path).unlink(missing_ok=True)
                
                except Exception as e:
                    st.error(f"❌ Error processing CV: {str(e)}")
                    st.exception(e)
    
    with tab2:
        st.header("📊 Results")
        
        if st.session_state.results:
            results = st.session_state.results
            
            # Metrics
            if show_metrics:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Baseline Similarity",
                        f"{results['baseline_similarity']:.2%}",
                        delta=None
                    )
                
                with col2:
                    st.metric(
                        "Final Similarity",
                        f"{results['final_similarity']:.2%}",
                        delta=f"{results['improvement']:+.2%}"
                    )
                
                with col3:
                    improvement_pct = (results['improvement'] / results['baseline_similarity'] * 100) if results['baseline_similarity'] > 0 else 0
                    st.metric(
                        "Improvement",
                        f"{results['improvement']:+.4f}",
                        delta=f"{improvement_pct:+.1f}%"
                    )
                
                with col4:
                    status = "✅ Improved" if results['improvement'] > 0 else "⚠️ No Improvement"
                    st.metric("Status", status)
            
            st.markdown("---")
            
            # Enhanced CV
            st.subheader("✨ Enhanced CV")
            st.markdown("**Preview:**")
            st.markdown(results['enhanced_cv'])
            
            # Download button
            st.download_button(
                label="📥 Download Enhanced CV (Markdown)",
                data=results['enhanced_cv'],
                file_name="enhanced_cv.md",
                mime="text/markdown"
            )
            
            # Keywords
            if show_keywords:
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📋 CV Keywords")
                    try:
                        cv_keywords = json.loads(results['cv_keywords'])
                        st.write(cv_keywords)
                    except:
                        st.code(results['cv_keywords'])
                
                with col2:
                    st.subheader("💼 Job Keywords")
                    try:
                        job_keywords = json.loads(results['job_keywords'])
                        st.write(job_keywords)
                    except:
                        st.code(results['job_keywords'])
        else:
            st.info("👈 Go to the 'Enhance CV' tab to process your CV")
    
    with tab3:
        st.header("ℹ️ About Knitty")
        
        st.markdown("""
        ### 🧵 What is Knitty?
        
        Knitty is an intelligent CV tailoring system that uses advanced AI to optimize your resume 
        for specific job postings. It analyzes your CV and the job requirements, then generates 
        an enhanced version that better aligns with what employers are looking for.
        
        ### ✨ Key Features
        
        - **🔄 Multi-LLM Architecture**: Uses specialized AI models for different tasks
        - **📊 Similarity Scoring**: Measures CV-job alignment using cosine similarity
        - **🎯 Smart Enhancement**: Generates tailored CVs while maintaining professional quality
        - **🔁 Iterative Improvement**: Automatically retries if similarity doesn't improve
        - **📱 Multiple Formats**: Export in Markdown and HTML formats
        
        ### 🚀 How It Works
        
        1. **Input Processing**: Extracts text from your CV PDF and processes the job posting
        2. **Keyword Analysis**: Extracts relevant keywords from both sources
        3. **Similarity Measurement**: Calculates how well your CV matches the job
        4. **Intelligent Enhancement**: Uses AI to optimize your CV while keeping it authentic
        5. **Quality Assurance**: Validates improvement and retries if needed
        
        ### 📈 Typical Results
        
        - Baseline similarity: 40-70%
        - Improvement: +5% to +15% increase
        - Processing time: ~30-60 seconds
        
        ### 🔒 Privacy
        
        Your CV and job posting data are processed securely and are not stored permanently.
        """)
        
        st.markdown("---")
        st.markdown("**Version:** 0.1.0")


if __name__ == "__main__":
    main()

