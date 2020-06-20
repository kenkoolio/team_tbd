from spliceAndProcess import Segment
from typing import List

def create_imagetext_dictionary(segments: List[Segment]):
    image_text=[]
    for segment in segments:
        image_text.append({
            'image' : segment.imagePath,
            'text' : segment.text
        })
    print(image_text)
    return image_text

def update_text(segments: List[Segment],image_text):
    for segment in segments:
        segment.text = image_text[segment.imagePath]
    return segments
