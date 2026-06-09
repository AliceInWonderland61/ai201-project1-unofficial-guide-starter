import gradio as gr
from generate import ask

custom_css = """
* {
    font-family: 'Georgia', serif;
    color: #2d1b4e;
}

body, .gradio-container {
    background-color: #b8a9c9 !important;
}

.gradio-container {
    max-width: 960px !important;
    margin: 0 auto !important;
    padding: 2rem !important;
}

.gradio-container > .block:first-child {
    background: none !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}

h1, h2, h3, h4, p, li, span, div, label, textarea, input, strong, em {
    color: #2d1b4e !important;
}

button.primary {
    background: linear-gradient(135deg, #e8a0bf, #c084c8) !important;
    border: none !important;
    color: #2d1b4e !important;
    font-size: 1rem !important;
    border-radius: 8px !important;
    font-family: 'Georgia', serif !important;
}

button.primary:hover {
    background: linear-gradient(135deg, #d4789a, #a855b5) !important;
}

label {
    color: #2d1b4e !important;
    font-weight: bold !important;
}

.question-box textarea {
    background-color: #f2d7e8 !important;
    border: 1.5px solid #c084c8 !important;
    border-radius: 8px !important;
    color: #2d1b4e !important;
}

.answer-box textarea {
    background-color: #d6e8f7 !important;
    border: 1.5px solid #7bafd4 !important;
    border-radius: 8px !important;
    color: #2d1b4e !important;
}

.sources-box textarea {
    background-color: #d6f0e8 !important;
    border: 1.5px solid #6abfa0 !important;
    border-radius: 8px !important;
    color: #2d1b4e !important;
}

.block {
    background-color: #cbbfdf !important;
    border: 1.5px solid #9b7fc4 !important;
    border-radius: 12px !important;
}

footer {
    display: none !important;
}
"""

def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources


with gr.Blocks(css=custom_css, title="CS Course Difficulty Guide") as demo:
    gr.Markdown("""
    # 🌙 The Unofficial CS Course Difficulty Guide
    
    ### Real answers from real students
    Ask anything about CS course difficulty — grounded in reviews from Reddit, Rate My Professors, and OMSCentral.
    
    **Try asking:** What CS courses do students agree are the hardest? · What courses should I avoid taking at the same time? · How does prior experience affect difficulty?
    """)

    inp = gr.Textbox(
        label="Your question",
        placeholder="e.g. What are the hardest CS courses across universities?",
        lines=2,
        elem_classes=["question-box"]
    )

    btn = gr.Button("Ask ✦", variant="primary")

    with gr.Row():
        with gr.Column(scale=3):
            answer = gr.Textbox(
                label="Answer",
                lines=12,
                elem_classes=["answer-box"]
            )
        with gr.Column(scale=1):
            sources = gr.Textbox(
                label="Sources",
                lines=12,
                elem_classes=["sources-box"]
            )

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()