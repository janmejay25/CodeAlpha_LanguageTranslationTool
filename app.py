import gradio as gr
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile

# Translation function
def translate_with_audio(text, source_lang, target_lang):
    if not text or not text.strip():
        return "", None
    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        result = translator.translate(text)
        
        # Generate audio
        tts = gTTS(text=result, lang=target_lang, slow=False)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        tts.save(temp_file.name)
        
        return result, temp_file.name
    except Exception as e:
        return f"⚠️ Error: {str(e)}", None

# Languages
LANGUAGES = [
    ("Auto Detect", "auto"), ("English", "en"), ("Spanish", "es"), 
    ("French", "fr"), ("German", "de"), ("Italian", "it"), 
    ("Portuguese", "pt"), ("Hindi", "hi"), ("Gujarati", "gu"), 
    ("Chinese", "zh-CN"), ("Japanese", "ja"), ("Korean", "ko"), 
    ("Russian", "ru"), ("Arabic", "ar"), ("Turkish", "tr"),
    ("Dutch", "nl"), ("Polish", "pl"), ("Indonesian", "id"),
    ("Vietnamese", "vi"), ("Thai", "th"), ("Bengali", "bn")
]
TARGET_LANGUAGES = [lang for lang in LANGUAGES if lang[1] != "auto"]

# CSS
css = """
* {font-family: 'Inter', sans-serif;}
.container {max-width: 1000px; margin: auto; padding: 2rem 1rem;}
.title {text-align: center; font-size: 3rem; font-weight: 300; color: #1f2937; letter-spacing: 0.1em;}
.subtitle {text-align: center; color: #6b7280; margin-bottom: 2rem;}
footer {visibility: hidden;}
"""

# Interface
with gr.Blocks(title="Bhasha Translation | CodeAlpha") as demo:
    with gr.Column(elem_classes="container"):
        gr.HTML("<h1 class='title'>भाषा</h1>")
        gr.HTML("<p class='subtitle'>Professional Language Translation • Google Translate API • Text-to-Speech</p>")
        
        with gr.Row():
            source_lang = gr.Dropdown(LANGUAGES, value="auto", label="From", scale=1)
            target_lang = gr.Dropdown(TARGET_LANGUAGES, value="hi", label="To", scale=1)
        
        input_text = gr.Textbox(label="Enter Text", placeholder="Type here...", lines=6)
        
        with gr.Row():
            clear_btn = gr.Button("Clear", variant="secondary", scale=1)
            translate_btn = gr.Button("Translate", variant="primary", scale=2)
        
        output_text = gr.Textbox(label="Translation", lines=6, interactive=False)
        audio_output = gr.Audio(label="Listen", type="filepath")
        
        gr.Examples(
            [
                ["Hello, how are you?", "auto", "hi"],
                ["Thank you for your help", "en", "es"],
                ["Where is the hospital?", "en", "gu"]
            ],
            [input_text, source_lang, target_lang]
        )
        
        gr.HTML("<p style='text-align: center; color: #9ca3af; margin-top: 2rem;'>Built by Janmejay Pandya • CodeAlpha 2025</p>")
    
    translate_btn.click(translate_with_audio, [input_text, source_lang, target_lang], [output_text, audio_output])
    clear_btn.click(lambda: ("", "", None), None, [input_text, output_text, audio_output])

if __name__ == "__main__":
    demo.launch(css=css)