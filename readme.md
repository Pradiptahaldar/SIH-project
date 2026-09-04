1. Education
2. Healthcare
3. Agriculture
4. Water Resources
5. Environment
6. Energy
7. Urban Development
8. Accessibility
9. Public Administration
10. Rural Livelihoods
                POST /analyze
                     │
             Challenge Submission
                     │
       ┌─────────────┼─────────────┐
       ↓             ↓             ↓
     Text          Image      Audio/Video
       │             │             │
       ↓             ↓             ↓
   NLP module    Vision module   Speech/Video
       │             │             │
       └─────────────┼─────────────┘
                     ↓
              Unified Analysis
                     │
          ┌──────────┼──────────┐
          ↓          ↓          ↓
      Category    Priority   Duplicate
USER SUBMISSION
      │
      ├── Text ───────────────┐
      │                       │
      ├── Image → description ┤
      │                       │
      ├── Audio → transcript ─┤
      │                       ↓
      └── Video → analysis ──→ COMBINED TEXT
                              │
                              ↓
                         CATEGORIZER
                              │
                              ↓
                   Category + Confidence


uvicorn app.main:app --reload
{
  "challenge": "Many students in rural areas do not have access to quality digital education."
}
python -m tests.test_pipeline
python -m tests.test_multimodal
python tests/test_multimodal_pipeline.py
python -m tests.test_multimodal_pipeline
Many rural communities face delays in adopting solar energy because there are not enough trained workers available to properly install and maintain solar panel systems.