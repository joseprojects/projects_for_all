import random
import requests
from PIL import Image, ImageDraw, ImageFont


# ==========================
# Agent: InstagramAccountAgent
# ==========================
class InstagramAccountAgent:
    def __init__(self):
        """
        In a real application, load your Instagram Business Account credentials.
        For Instagram Graph API, you need:
          - IG_USER_ID: Your Instagram Business Account ID.
          - ACCESS_TOKEN: A valid access token with permissions to publish content.
        These should be securely stored (e.g., in environment variables).
        """
        self.ig_user_id = "YOUR_IG_BUSINESS_USER_ID"
        self.access_token = "YOUR_ACCESS_TOKEN"

    def get_credentials(self):
        creds = {
            "ig_user_id": self.ig_user_id,
            "access_token": self.access_token
        }
        print(f"[InstagramAccountAgent] Loaded credentials: {creds}")
        return creds


# ==========================
# Agent: ImageBuilderAgent
# ==========================
class ImageBuilderAgent:
    def build_image(self, text):
        """
        Build an image using Pillow. This image is saved locally.
        In production, you'll need to upload this image to a public hosting service.
        """
        width, height = 400, 400
        # Generate a random background color
        bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        image = Image.new("RGB", (width, height), color=bg_color)
        draw = ImageDraw.Draw(image)

        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except IOError:
            font = ImageFont.load_default()

        text_width, text_height = draw.textsize(text, font=font)
        text_x = (width - text_width) / 2
        text_y = (height - text_height) / 2
        draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)

        image_path = "post_image.png"
        image.save(image_path)
        print(f"[ImageBuilderAgent] Image created and saved as {image_path}")
        return image_path


# ==========================
# Agent: PromptCreationAgent
# ==========================
class PromptCreationAgent:
    def create_prompt(self):
        """
        Generate a caption/prompt for the Instagram post.
        You could integrate a language model API here for dynamic content.
        """
        prompts = [
            "Hello Instagram! This is an automated business post.",
            "Exploring automation on Instagram Business accounts.",
            "Bringing AI to social media—one post at a time!",
            "Automated posting via the Instagram Graph API."
        ]
        prompt = random.choice(prompts)
        print(f"[PromptCreationAgent] Generated prompt: {prompt}")
        return prompt


# ==========================
# Agent: PostingAgent
# ==========================
class PostingAgent:
    def __init__(self, ig_credentials):
        self.ig_user_id = ig_credentials["ig_user_id"]
        self.access_token = ig_credentials["access_token"]
        # Base URL for Graph API (version may vary)
        self.base_url = "https://graph.facebook.com/v14.0"

    def upload_image_to_hosting(self, local_image_path):
        """
        In a production scenario, upload your image file to a public hosting service.
        For demonstration, assume you have an image URL after upload.
        Replace this method with actual upload logic.
        """
        # Simulated public URL after upload; replace with real upload code.
        public_image_url = "https://your-public-host.com/path/to/post_image.png"
        print(f"[PostingAgent] Simulated image upload. Public URL: {public_image_url}")
        return public_image_url

    def create_media_container(self, image_url, caption):
        """
        Call the Instagram Graph API to create a media container.
        Documentation:
          https://developers.facebook.com/docs/instagram-api/guides/content-publishing/
        """
        endpoint = f"{self.base_url}/{self.ig_user_id}/media"
        payload = {
            "image_url": image_url,
            "caption": caption,
            "access_token": self.access_token
        }
        print(f"[PostingAgent] Creating media container with payload: {payload}")
        response = requests.post(endpoint, data=payload)
        if response.status_code == 200:
            creation_id = response.json().get("id")
            print(f"[PostingAgent] Media container created with ID: {creation_id}")
            return creation_id
        else:
            print(f"[PostingAgent] Failed to create media container: {response.text}")
            return None

    def publish_media(self, creation_id):
        """
        Publish the media container to your Instagram feed.
        """
        endpoint = f"{self.base_url}/{self.ig_user_id}/media_publish"
        payload = {
            "creation_id": creation_id,
            "access_token": self.access_token
        }
        print(f"[PostingAgent] Publishing media with payload: {payload}")
        response = requests.post(endpoint, data=payload)
        if response.status_code == 200:
            post_id = response.json().get("id")
            print(f"[PostingAgent] Media published with post ID: {post_id}")
            return post_id
        else:
            print(f"[PostingAgent] Failed to publish media: {response.text}")
            return None

    def post_content(self, image_local_path, caption):
        """
        Complete posting: upload image, create media container, and publish it.
        """
        # 1. Upload the image and obtain a public URL
        image_url = self.upload_image_to_hosting(image_local_path)

        # 2. Create media container
        creation_id = self.create_media_container(image_url, caption)
        if not creation_id:
            return {"status": "failure", "error": "Failed to create media container"}

        # 3. Publish the media container
        post_id = self.publish_media(creation_id)
        if post_id:
            return {"status": "success", "post_id": post_id}
        else:
            return {"status": "failure", "error": "Failed to publish media"}


# ==========================
# Agent: NotificationAgent
# ==========================
class NotificationAgent:
    def send_notification(self, message):
        """
        Notify you that the Instagram post has been made.
        In production, this might send an email, SMS, or push notification.
        """
        print(f"[NotificationAgent] Notification: {message}")


# ==========================
# Main Agent Controller
# ==========================
def main():
    print("Starting Instagram Business Account Automation Agent...\n")

    # 1. Load preconfigured Instagram account credentials
    account_agent = InstagramAccountAgent()
    ig_credentials = account_agent.get_credentials()

    # 2. Generate a caption/prompt for the post
    prompt_agent = PromptCreationAgent()
    caption = prompt_agent.create_prompt()

    # 3. Create an image using the caption (or any desired text)
    image_agent = ImageBuilderAgent()
    image_local_path = image_agent.build_image(caption)

    # 4. Post the content via Instagram Graph API
    posting_agent = PostingAgent(ig_credentials)
    post_response = posting_agent.post_content(image_local_path, caption)

    # 5. Notify you that the post has been made
    notification_agent = NotificationAgent()
    if post_response.get("status") == "success":
        notification_agent.send_notification(
            f"Instagram post made successfully! Post ID: {post_response.get('post_id')}"
        )
    else:
        notification_agent.send_notification(
            f"Failed to post on Instagram: {post_response.get('error')}"
        )


if __name__ == "__main__":
    main()