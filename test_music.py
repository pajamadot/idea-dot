from music_generation import generate_music

def test_music_generation():
    prompt = "Upbeat EDM at 128 BPM with punchy bass and bright synths"
    print("Testing music generation...")
    result = generate_music(prompt, duration=6)
    if result:
        print(f"Success! Generated music saved to: {result}")
    else:
        print("Music generation failed.")

if __name__ == "__main__":
    test_music_generation() 