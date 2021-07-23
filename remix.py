from sklearn.neighbors import NearestNeighbors

from infiniteremixer.data.createdataset import _create_data_pipeline
from infiniteremixer.remix.generateremix import _create_objects
from infiniteremixer.segmentation.segmentextractor import SegmentExtractor
from infiniteremixer.utils.io import load_from_pickle, save_to_pickle, write_wav

# PATHS
AUDIOS_PATH = "results/audios"
SEGMENTS_PATH = "results/segmented"
DATASET_PATH = "results/dataset"
NEAREST_NEIGHBOUR_PATH = "results/model/model.pkl"

REMIX_PATH = "results/remix/remix.wav"
SAMPLE_RATE = 22050
# PARAMETERS FOR GENERATION
JUMP_RATE = 0.005
NUM_BEATS = 60

# Segment
segment_extractor = SegmentExtractor(SAMPLE_RATE)
segment_extractor.create_and_save_segments(
    AUDIOS_PATH,
    SEGMENTS_PATH,
)
# Extract and aggreagate features
data_pipeline = _create_data_pipeline()
data_pipeline.process(
    SEGMENTS_PATH,
    DATASET_PATH,
)
# Fit nearest neighbors
dataset = load_from_pickle(f"{DATASET_PATH}/dataset.pkl")
print(f"Loaded dataset from {DATASET_PATH}/dataset.pkl")
print(f"Dataset array has shape {dataset.shape}")
nearest_neighbour = NearestNeighbors()
nearest_neighbour.fit(dataset)
print("Created nearest neighbour")
save_to_pickle(NEAREST_NEIGHBOUR_PATH, nearest_neighbour)
print(f"Saved nearest neighbour model to {NEAREST_NEIGHBOUR_PATH}")
# Generate remix
remixer, chunk_merger = _create_objects(JUMP_RATE, NUM_BEATS)
remix = remixer.generate_remix()
print(f"Generated remix with {NUM_BEATS} beats")
audio_remix = chunk_merger.concatenate(remix.file_paths)
print(f"Merged beats together")
write_wav(REMIX_PATH, audio_remix, SAMPLE_RATE)
print(f"Saved new remix to {SAMPLE_RATE}")
