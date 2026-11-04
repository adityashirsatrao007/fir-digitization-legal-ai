# Training Datasets

**The training images are not committed to this repository** (they are
third-party scanned FIR documents and are not redistributable). Only the
directory layout and label schema are documented here, so a model can be
retrained by dropping the corpus back in.

`demo_firs/` at the repo root holds a few sample documents that the demo uses.

## Contents

### fir_documents/
Scanned FIR (First Information Report) documents used for OCR training. Contains
annotated images with bounding boxes for key fields like police station name,
year, statutes, and complainant details, plus `FIR_details.json` with the labels.

### yolo_training/
YOLO format dataset for object detection training. Split into train/val sets with
corresponding labels.

## Notes
- Images are preprocessed and standardized
- Annotations are in JSON and YOLO txt formats
- See individual folder READMEs for detailed documentation
