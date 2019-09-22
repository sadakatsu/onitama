# Onitama

This project is intended to train a deep learning model to play [Onitama](https://www.arcanewonders.com/game/onitama/).
My hope is to use this as a test project to refine my understanding of deep learning systems and reinforcement learning
while making something that I find interesting.  I also intend to use this to experiment with an iterative reinforcement
learning approach that I have in mind for future, more ambitious projects.

The steps planned for this project are:

1. Implement the rules for the core Onitama game (no expansion packs), with one added rule that entering a cycle forces
   forces a draw.
2. Implement a random agent that will form the initial strawman to beat.
3. Build a simple interface to allow playing Onitama with different settings (human v. human, human v. AI, or AI v. AI)
   and to load and review game records. (Might defer until later)
4. Implement a UCTS-style tree search.
5. Design the deep learning network.  My current idea is to create a simple vector encoding of the game state, use a FCL
   to transform that vector into a 5x5 grid (possibly with multiple channels), nine residual blocks with either 32 or 64
   features using 3x3 convolutions, then having a value head (FCL into five softmax outputs that represent the
   probabilities of the five outcomes) and a policy head (FCL into a layer that is multiplied with an initial feature
   vector that indicates which of the 903 possible moves are legal, then softmaxed into exploration probabilities).
6. Test the UCTS with a randomly generated, untrained model.
7. Refine the process of transforming the search trees developed from playouts into reinforcement training sets.
8. Iteratively fresh train models to try to surpass the previous set of agents (starting with only the random agent) to
   try to achieve at least a 100-point Elo improvement over the last best agent until it appears that the best previous
   agent can at best be tied.
9. (Optional) Train a new policy head based off of the final agent's stack to estimate the weakest and strongest strengths of
   players that pick a certain move using data from one final tournament.
10. (Optional) Devise a way to use the policy head from #9 to figure out how strong I am.
