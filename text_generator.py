import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import LambdaCallback

# Load and preprocess the text data
text = open("text_data.txt", "r").read()
text = text.lower()

# Create character-level mappings
chars = sorted(list(set(text)))
char_to_idx = {char: idx for idx, char in enumerate(chars)}
idx_to_char = {idx: char for idx, char in enumerate(chars)}

# Prepare the training data
max_len = 40
step = 3
sentences = []
next_chars = []
for i in range(0, len(text) - max_len, step):
    sentences.append(text[i : i + max_len])
    next_chars.append(text[i + max_len])
    
# Vectorize the training data
X = np.zeros((len(sentences), max_len, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        X[i, t, char_to_idx[char]] = 1
    y[i, char_to_idx[next_chars[i]]] = 1

# Define the LSTM model
model = Sequential()
model.add(LSTM(128, input_shape=(max_len, len(chars))))
model.add(Dense(len(chars), activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')

# Function to sample the next character
def sample_next_char(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

# Function to generate text at each epoch
def on_epoch_end(epoch, _):
    print('\n----- Generating text after Epoch: %d' % epoch)
    start_index = np.random.randint(0, len(text) - max_len - 1)
    generated_text = text[start_index : start_index + max_len]
    print('----- Seed text: "' + generated_text + '"')
    
    for temperature in [0.2, 0.5, 1.0, 1.2]:
        print('\n----- Temperature:', temperature)
        output_text = generated_text
        for _ in range(400):
            sampled = np.zeros((1, max_len, len(chars)))
            for t, char in enumerate(generated_text):
                sampled[0, t, char_to_idx[char]] = 1.
                
            preds = model.predict(sampled, verbose=0)[0]
            next_index = sample_next_char(preds, temperature)
            next_char = idx_to_char[next_index]
            
            generated_text += next_char
            generated_text = generated_text[1:]
            
            output_text += next_char
        print(output_text)

# Train the model
model.fit(X, y, batch_size=128, epochs=20, callbacks=[LambdaCallback(on_epoch_end=on_epoch_end)])


