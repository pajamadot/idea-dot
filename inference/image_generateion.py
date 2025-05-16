import logging

import fal_client
from typing import Any, TypedDict, cast

logger = logging.getLogger(__name__)

class FalImage(TypedDict):
    """Type definition for image response from FAL API
    
    Attributes:
        url: URL of the generated image
        width: Width of the image in pixels
        height: Height of the image in pixels 
        content_type: MIME type of the image
    """
    url: str
    width: int
    height: int
    content_type: str

class FalResponse(TypedDict):
    """Type definition for FAL API response
    
    Attributes:
        images: List of generated images
    """
    images: list[FalImage]

async def fal_image_api_call(model_id: str, arguments: dict[str, Any]) -> FalResponse:
    """Makes an asynchronous API call to FAL's image generation service
    
    Args:
        model_id: ID of the FAL model to use
        arguments: Dictionary of arguments to pass to the model
        
    Returns:
        FalResponse containing the generated images
        
    Logs all generation events for monitoring
    """
    handler = await fal_client.submit_async(model_id, arguments=arguments)
    async for event in handler.iter_events(with_logs=True):
        logger.info(f"Generation event: {event}")
    result = await handler.get()
    return cast(FalResponse, result)

async def generate_character(prompt: str):
    """Generate a character based on text prompt
    
    Uses the schnell model which is optimized for fast character generation
    
    Args:
        prompt: Text description of the character to generate
        
    Returns:
        FalResponse containing the generated character image
    """
    return await fal_image_api_call(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": prompt,
            "image_size": "square_hd",
            "num_images": 1,
            "format": "jpeg"
        }
    )


# To keep the characater looking consisitent
# here we use pulid model to fast generate a character from a reference image 
# we will use character LORA to generate the characters with future generations.
async def generate_character_use_ref(prompt: str, reference_image: str):
    """Generate a character based on text prompt and reference image
    
    Uses the pulid model which can maintain consistency with a reference image.
    This helps generate variations of an existing character.
    
    Args:
        prompt: Text description of the character to generate
        reference_image: URL of the reference image to base generation on
        
    Returns:
        FalResponse containing the generated character image that maintains
        consistency with the reference
    """
    return await fal_image_api_call(
        "fal-ai/flux-pulid",
        arguments={
            "prompt": prompt,
            "reference_image_url": reference_image,
            "image_size": "square_hd",
            "num_images": 1,
            "format": "jpeg"
        }
    )

async def generate_planet(prompt: str):
    """Generate a planet based on text prompt
    
    Uses the flux model which is good for generating detailed landscapes and environments
    
    Args:
        prompt: Text description of the planet to generate
        
    Returns:
        FalResponse containing the generated planet image
    """
    return await fal_image_api_call(
        "fal-ai/flux",
        arguments={
            "prompt": f"a detailed view of a planet from space, {prompt}, cinematic lighting, highly detailed, 8k",
            "image_size": "landscape_16_9",
            "num_images": 1,
            "format": "jpeg"
        }
    )

if __name__ == "__main__":
    import asyncio
    
    async def test_generation():
        initial_prompt = input("Enter initial character prompt: ")
        
        print("Generating initial character...")
        initial_result = await generate_character(initial_prompt)
        initial_image_url = initial_result["images"][0]["url"]
        print(f"Initial character generated at: {initial_image_url}")
        
        # Get reference prompt from user
        reference_prompt = input("Enter prompt for reference-based generation: ")
        
        # Generate character using reference
        print("Generating character from reference...")
        reference_result = await generate_character_use_ref(reference_prompt, initial_image_url)
        reference_image_url = reference_result["images"][0]["url"]
        print(f"Reference-based character generated at: {reference_image_url}")

    asyncio.run(test_generation())
