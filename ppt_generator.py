from pptx import Presentation


def create_presentation(slides_content):

    prs = Presentation()

    slides = slides_content.split(
        "================================================"
    )

    for slide_text in slides:

        if not slide_text.strip():
            continue

        slide = prs.slides.add_slide(
            prs.slide_layouts[1]
        )

        title = "Presentation Slide"

        if "TITLE:" in slide_text:

            try:

                title = (
                    slide_text.split(
                        "TITLE:"
                    )[1]
                    .split("\n")[0]
                    .strip()
                )
            except:
                pass

        slide.shapes.title.text = title

        slide.placeholders[
            1
        ].text = slide_text

    file_name = (
        "AI_Requirement_Presentation.pptx"
    )

    prs.save(file_name)

    return file_name
