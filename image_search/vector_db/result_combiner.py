from typing import List, Dict

from image_search.vector_db.imagedb_schema import FIELD_IMAGE_NAME


def combine_results(res_image: List[Dict], res_text: List[Dict], limit: int):
    def rank_results(res: List[Dict]):
        return {
            r[FIELD_IMAGE_NAME]: {**r, "rank_points": limit - i}
            for i, r in enumerate(res)
        }

    ranked_images = rank_results(res_image)
    ranked_text = rank_results(res_text)

    combined_dict = {image_name: value for image_name, value in ranked_images.items()}

    for image_name, value in ranked_images.items():
        if image_name not in ranked_text:
            print(f"Image result not ranked: {image_name}")
            value["rank_points"] = value["rank_points"] / 2 # Only available as text result. Divide by two to penalize

    for image_name, value in ranked_text.items():
        if image_name not in combined_dict:
            print(f"Text result not ranked: {image_name}")
            combined_dict[image_name] = value
            value["rank_points"] = value["rank_points"] / 2 # Only available as text result. Divide by two to penalize
        else:
            item = combined_dict[image_name]
            item["rank_points"] = item["rank_points"] + value["rank_points"]
            if "_distance" in item:
                item["_distance"] = (item["_distance"] + value["_distance"]) / 2

    return sorted(combined_dict.values(), key=lambda x: x["rank_points"], reverse=True)
