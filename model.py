import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class LinearQNet(nn.Module):
    def __init__(self, inputSize, hiddenSize, outputSize):
        super().__init__()
        self.linear1 = nn.Linear(inputSize, hiddenSize)
        self.linear2 = nn.Linear(hiddenSize, outputSize)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x
    
    def save(self, fileName="Model.pth"):
        modelFolderPath = "./model"
        if not os.path.exists(modelFolderPath):
            os.makedirs(modelFolderPath)

        fileName = os.path.join(modelFolderPath, fileName)
        torch.save(self.state_dict(), fileName)

    def load(self, fileName="Model.pth"):
        modelFolderPath = "./model"
        if os.path.exists(modelFolderPath):
            fileName = os.path.join(modelFolderPath, fileName)
            self.load_state_dict(torch.load(fileName))
            self.eval()

class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criteria = nn.MSELoss()

    def trainStep(self, state, action, reward, nextState, done):
        state = torch.tensor(state, dtype = torch.float)
        action = torch.tensor(action, dtype = torch.float)
        reward = torch.tensor(reward, dtype = torch.float)
        nextState = torch.tensor(nextState, dtype = torch.float)

        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            nextState = torch.unsqueeze(nextState, 0)
            done = (done, )

            # get predicted Q values with currrent state
            prediction = self.model(state)

            target = prediction.clone()
            # my done is in reverse since I use my 'running' bool
            # normally do 'not done' instead
            for i in range(len(done)):
                qNew = reward[i]
                if done[i]:
                    qNew = reward[i] + self.gamma * torch.max(self.model(nextState[i]))

                target[i][torch.argmax(action).item()] = qNew
            # Q-new = Reward + gamma + max (prediciton Q value) -> only if not done
            # pred.clone()
            # preds[argmax(action)] = q_new
                
            self.optimizer.zero_grad() # have to do this
            loss = self.criteria(target, prediction)
            loss.backward() # backwards propagation
            self.optimizer.step()
