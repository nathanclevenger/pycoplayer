# pycoplayer
Pycoplayer is a general AI that learns how to play games through trial and error, based on the visual and auditory output from any game of your choosing, it delivers keyboard, mouse, and controller input to play.

## Training via GitHub Actions
A workflow file located at `.github/workflows/train.yml` can be used to train the agent automatically. The job expects a **self‑hosted GPU runner** to maximise training performance. Trigger the workflow manually or whenever Python files change.

## Suggested optimizations
- Run training on a GPU enabled runner for faster neural network inference.
- Periodically save and load model checkpoints to resume interrupted runs.
- Experiment with techniques like prioritized experience replay or double DQN to improve learning stability.
