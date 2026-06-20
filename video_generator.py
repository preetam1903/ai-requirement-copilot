from moviepy import (
    ImageClip,
    AudioFileClip
)


def generate_training_video(
    avatar_image,
    narration_mp3,
    output_file="training_video.mp4"
):
    """
    Create simple training video.

    Avatar Image
    +
    Narration MP3
    =
    MP4
    """

    audio = AudioFileClip(
        narration_mp3
    )

    duration = audio.duration

    video = (
        ImageClip(
            avatar_image
        )
        .with_duration(
            duration
        )
        .with_audio(
            audio
        )
    )

    video.write_videofile(
        output_file,
        fps=24
    )

    return output_file
