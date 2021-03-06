# Deep Learning with Pytorch
# Module 6: Recurrent Neural Network
# MNIST classification with RNN

import torch
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F

# Step 1: Setup
torch.manual_seed(1)    # reproducible

# Hyper Parameters
EPOCH = 1               # train the training data n times, to save time, we just train 1 epoch
BATCH_SIZE = 64
RNN_SIZE = 64           # rnn hidden units
TIME_STEP = 28          # run time step / image height
INPUT_SIZE = 28         # rnn input size / image width
LR = 0.01               # learning rate

train_data = torchvision.datasets.MNIST(
    root='./mnist/', 
    train=True, 
    download=True, 
    transform=transforms.ToTensor())
train_loader = torch.utils.data.DataLoader(
    train_data, 
    batch_size=BATCH_SIZE, 
    shuffle=True, 
    num_workers=2)

test_data = torchvision.datasets.MNIST(
    root='./mnist/', 
    train=False,
    download=True, 
    transform=transforms.ToTensor())
test_loader = torch.utils.data.DataLoader(
    test_data, 
    batch_size=BATCH_SIZE, 
    shuffle=True, 
    num_workers=2)

# Step 2: Model
class RNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.rnn = nn.RNN(         
            input_size=INPUT_SIZE,
            hidden_size=RNN_SIZE,   
            num_layers=1,           
            batch_first=True,       
        )

        self.fc = nn.Linear(RNN_SIZE, 10)

    def forward(self, x):
        x, h_n = self.rnn(x, None)   # None represents zero initial hidden state
        x = self.fc(x[:, -1, :])     # seq_len, batch, hidden_size * num_directions
        return x


rnn = RNN()
print(rnn)

# Step 3: Loss Function
loss_func = nn.CrossEntropyLoss()                      

# Step 4: Optmizer
optimizer = torch.optim.Adam(rnn.parameters(), lr=LR)   


# Step 5: Training Loop
correct = 0
total = 0
for epoch in range(EPOCH):
    for i, (x, y) in enumerate(train_loader):   
        x = Variable(x.view(-1, TIME_STEP, INPUT_SIZE))    # reshape x to (batch, time_step, input_size)  
        y = Variable(y)

        yhat = rnn(x)
        loss = loss_func(yhat, y)           # cross entropy loss

        optimizer.zero_grad()               # clear gradients for this training step
        loss.backward()                     # backpropagation, compute gradients
        optimizer.step()                    # apply gradients

        _, y_pred = torch.max(yhat.data, 1)
        total += y.size(0)
        correct += (y_pred == y.data).sum()
        if i % 10 == 0:
            print('Epoch/Step: ', epoch, '/',i, 
                '| train loss: %.4f' % loss.data[0], 
                '| accuracy: %.2f %%' % (100 * correct / total))

#Step 6: Evaluation
correct = 0
total = 0
for (x,y) in test_loader:
    x = Variable(x.view(-1, TIME_STEP, INPUT_SIZE))           
    y = Variable(y)

    yhat = rnn(x)
    _, y_pred = torch.max(yhat.data, 1)
    total += y.size(0)
    correct += (y_pred == y.data).sum()
print('Test accuracy: %.2f %%' % (100 * correct / total))

