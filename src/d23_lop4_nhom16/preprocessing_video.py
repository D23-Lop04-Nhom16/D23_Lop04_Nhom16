#type: ignore

from vid_prepper import metadata 

# Extract metadata
video_path = ["/home/ninhdao/D23_Lop4_Nhom16/videos/dog.mp4"]
video_info = metadata.Metadata.validate_videos(video_path)

print(video_info)
