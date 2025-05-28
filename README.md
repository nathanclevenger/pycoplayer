# pycoplayer
Pycoplayer is a general AI that learns how to play games through trial and error, based on the visual and auditory output from any game of your choosing, it delivers keyboard, mouse, and controller input to play.

## Training via GitHub Actions
A workflow at `.github/workflows/train.yml` runs training on a standard GitHub Actions runner using only the CPU. Trigger the workflow manually or whenever Python files change. For faster learning you may configure your own GPU runner.

## Suggested optimizations
- Run training on a GPU enabled runner for faster neural network inference.
- Periodically save and load model checkpoints to resume interrupted runs.
- Experiment with techniques like prioritized experience replay or double DQN to improve learning stability.
