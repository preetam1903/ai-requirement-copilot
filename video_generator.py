from moviepy import (
    ImageClip,
    AudioFileClip
)


def generate_training_video(
    avatar_image,
    narration_mp3,
    output_file="training_video.mp4"
):

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
    )

    final_video = (
        video.with_audio(
            audio
        )
    )

    final_video.write_videofile(
        output_file,
        codec="libx264",
        audio_codec="aac",
        fps=24
    )

    return output_file
