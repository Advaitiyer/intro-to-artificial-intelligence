#!/usr/bin/python
# -*- coding: utf-8 -*-
# from othello_rules import *
from othello_net import *
from tensorflow.python.framework import ops
from datetime import datetime
from feature_extractor import *
from training_utils import *
import numpy as np
import hashlib, random

start_eta = 3e-5
#iterations = 1000

def avg_error(data_path, sess, len_games = 16):
    errors = []
    validation_matches = get_all_matches(data_path)
    validation_matches = validation_matches[0:len_games]
    for i in range(len(validation_matches)):
        unpacked_movelist = unpack_movelist(validation_matches[i])
        board, player, previous_moves_avg = initialize_game_full()
        for move in unpacked_movelist:
            if move == 0:
                break
            feature_path = '/storage/hlynur/cache/validation/features/features_' + str(i) + "_" + str(move) + ".npy"
            label_path = '/storage/hlynur/cache/validation/labels/labels_' + str(i) + "_" + str(move) + ".npy"
            features, label = fetch_or_calculate_planes(board, player, previous_moves_avg, move,
                                                        feature_path, label_path, fetch=True)
            input_batch = [features]
            label_batch = [label]
            error = sess.run(loss, feed_dict={img_data:input_batch, ground_truths: label_batch})
            errors.append(error)
            board = make_move(board, move, player)
            player, legal_moves, previous_moves_avg = update_states(player, board, move, previous_moves_avg)
    return np.sum(errors) / len(errors)

def prediction_accuracy(data_path, len_games=16):
    successes = []
    validation_matches = get_all_matches(data_path)
    #validation_matches = validation_matches[0:len_games]
    #for i in range(len_games):
    for i in range(len(validation_matches)):
        if (i+1) % 100 is 0:
            print(i)
        unpacked_movelist = unpack_movelist(validation_matches[i])
        board, player, previous_moves_pred = initialize_game_full()
        success= 0
        for move in unpacked_movelist:
            if move == 0:
                break
            feature_path = '/storage/hlynur/cache/validation/features/features_' + str(i) + "_" + str(move) + ".npy"
            label_path = '/storage/hlynur/cache/validation/labels/labels_' + str(i) + "_" + str(move) + ".npy"
            features, label = fetch_planes(move, feature_path, label_path)
            input_batch = [features]
            label_batch = [label]
            prediction = sess.run(pred_up, feed_dict={img_data:input_batch, ground_truths: label_batch})
            prediction = np.transpose(prediction[0])
            prediction = np.transpose(prediction[1])
            cleaned_predictions = zero_illegal_moves(prediction, find_legal_moves(board, player))
            pred_row, pred_col = np.unravel_index(cleaned_predictions.argmax(), cleaned_predictions.shape)
            move_argmax = str((pred_row+1) * 10 + (pred_col+1))
            if str(move) == str(move_argmax):
                success += 1
            success = check_rotational_invariance(board, move, move_argmax, success)
            board = make_move(board, move, player)
            player, legal_moves, previous_moves_pred = update_states(player, board, move, previous_moves_pred)
        successes.append(success)
    return np.mean(successes)

ops.reset_default_graph()
graph, img_data, train_step, optimizer, ground_truths, loss, pred_up, learn_rate, score_out = create_othello_net()
sess = tf.Session(config=tf.ConfigProto(log_device_placement=False))
init_op = tf.global_variables_initializer()
sess.run(init_op)
current_model = "models/layers8filters64.ckpt"
saver = tf.train.Saver()
if os.path.isfile(current_model + ".meta"):
    print("locked and loaded")
    saver.restore(sess, current_model)
validation_path = "/storage/hlynur/unprocessed/validation/"
matches = get_all_matches('/storage/hlynur/unprocessed/training/')
lenmatches = len(matches)
print("start training")
iterations = 12 * lenmatches
#iterations = 1
prev_stop = 0
input_batch = []
label_batch = []
for ite in range(prev_stop, prev_stop+iterations):
    i = ite % lenmatches
    unpacked_movelist = unpack_movelist(matches[i]) 
    # One training batch is all the data from one match
    for move in unpacked_movelist:
        if move == 0:
            break
        if random.randint(0, 100) < 50:
            continue
        feature_path = '/storage/hlynur/cache/training/features/features_' + str(i) + "_" + str(move) + ".npy"
        label_path = '/storage/hlynur/cache/training/labels/labels_' + str(i) + "_" + str(move) + ".npy"
        features, label = fetch_planes(move, feature_path, label_path)
        input_batch.append(features)
        label_batch.append(label)
        input_batch, label_batch = add_flips(input_batch, label_batch, features, move)
        #board = make_move(board, move, player)
        #player, legal_moves, previous_moves = update_states(player, board, move, previous_moves)
    eta = start_eta        
    train_step.run(session=sess, feed_dict={img_data:input_batch, ground_truths: label_batch,
                                             learn_rate:eta})
    input_batch = []
    label_batch = []
    games_to_batch = 0
        
    if (i % 20 is 0) and (i > 0 and i < 101) or (i+1) == (iterations+prev_stop) or (i % 2000 is 0):  
        log_time = datetime.now().strftime("%d. %b %H:%M:%S")
        log_acc = prediction_accuracy(validation_path)/float(60)
        log_loss = avg_error(validation_path, sess)
        log_experiment("logs.txt", log_time, log_acc, log_loss, i)
        save_path = saver.save(sess, current_model)

print("done")
