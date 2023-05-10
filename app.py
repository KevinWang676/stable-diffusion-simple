import gradio as gr
import os
from share_btn import community_icon_html, loading_icon_html, share_js

text_gen = gr.Interface.load(name="spaces/Gustavosta/MagicPrompt-Stable-Diffusion")
stable_diffusion = gr.Blocks.load(name="spaces/runwayml/stable-diffusion-v1-5")

def get_images(prompt):
    gallery_dir = stable_diffusion(prompt, fn_index=2)
    sd_output = [os.path.join(gallery_dir, image) for image in os.listdir(gallery_dir)]
    return sd_output, gr.update(visible=True), gr.update(visible=True), gr.update(visible=True)

def get_prompts(prompt_text):
    return text_gen(prompt_text)

css = '''
.animate-spin {
    animation: spin 1s linear infinite;
}
@keyframes spin {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
}
#share-btn-container {
    display: flex; padding-left: 0.5rem !important; padding-right: 0.5rem !important; background-color: #000000; justify-content: center; align-items: center; border-radius: 9999px !important; width: 13rem;
}
#share-btn {
    all: initial; color: #ffffff;font-weight: 600; cursor:pointer; font-family: 'IBM Plex Sans', sans-serif; margin-left: 0.5rem !important; padding-top: 0.25rem !important; padding-bottom: 0.25rem !important;
}
#share-btn * {
    all: unset;
}
#share-btn-container div:nth-child(-n+2){
    width: auto !important;
    min-height: 0px !important;
}
#share-btn-container .wrap {
    display: none !important;
}
a {text-decoration-line: underline;}
'''

with gr.Blocks(css=css) as demo:
    gr.HTML("""<div style="text-align: center; max-width: 700px; margin: 0 auto;">
            <div
            style="
                display: inline-flex;
                align-items: center;
                gap: 0.8rem;
                font-size: 1.75rem;
            "
            >
            <h1 style="font-weight: 900; margin-bottom: 7px; margin-top: 5px;">
                Magic Diffusion 🪄
            </h1>
            </div>
            <p style="margin-bottom: 10px; font-size: 94%">
            This Space prettifies your prompt using <a href="https://huggingface.co/spaces/Gustavosta/MagicPrompt-Stable-Diffusion" target="_blank">MagicPrompt</a>
            and then runs it through Stable Diffusion to create aesthetically pleasing images. Simply enter a few concepts and let it improve your prompt. You can then diffuse the prompt.
            </p>
        </div>""")

    with gr.Row():
      with gr.Column():
          input_text = gr.Textbox(label="Short text prompt", 
                                lines=4, elem_id="input-text")
          with gr.Row():
            see_prompts = gr.Button("Feed in your text!")

      with gr.Column():
        text_output = gr.Textbox(
                                label="Prettified text prompt", 
                                lines=4,
                                elem_id="translated"
                            )
        with gr.Row():
            diffuse_btn = gr.Button(value="Diffuse the Prompt!")
      with gr.Column(elem_id="generated-gallery"):
        sd_output = gr.Gallery().style(grid=2, height="auto")
        with gr.Group(elem_id="share-btn-container"):
            community_icon = gr.HTML(community_icon_html, visible=False)
            loading_icon = gr.HTML(loading_icon_html, visible=False)
            share_button = gr.Button("Share to community", elem_id="share-btn", visible=False)

    see_prompts.click(get_prompts, 
                            inputs = [input_text], 
                            outputs = [
                                text_output
                            ])
    diffuse_btn.click(get_images, 
                          inputs = [
                              text_output
                              ], 
                          outputs = [sd_output, community_icon, loading_icon, share_button]
                          )
    share_button.click(None, [], [], _js=share_js)



demo.launch(debug=True)
