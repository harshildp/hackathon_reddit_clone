''' @app.route('/wall')
def wall():
    query = 'SELECT message, CONCAT(first_name, " ", last_name) as name, date_format(messages.created_at, \"%M %D, %Y %r") as time, messages.id FROM users JOIN messages ON messages.user_id = users.id ORDER BY created_at DESC'
    messages = mysql.query_db(query)

    query = 'SELECT comment, CONCAT(first_name, " ", last_name) as name, date_format(comments.created_at, \"%M %D, %Y %r") as time, messages.id, comments.message_id, comments.id FROM users JOIN comments ON users.id = comments.user_id JOIN messages on messages.id = comments.message_id ORDER BY comments.created_at'
    comments = mysql.query_db(query)

    return render_template('wall.html', messages=messages, comments=comments) '''


''' @app.route('/post', methods=['POST'])
def post():
    message = request.form['message']
    query = 'INSERT INTO messages(message, user_id, created_at, updated_at) VALUES(:message, :user_id, NOW(), NOW())'
    data = {
        'message': message,
        'user_id': session['id']
    }
    mysql.query_db(query, data)
    return redirect('/wall')


@app.route('/comment/<message_id>', methods=['POST'])
def comment(message_id):
    comment = request.form['comment']
    query = 'INSERT INTO comments(comment, user_id, message_id, created_at, updated_at) VALUES(:comment, :user_id, :message_id, NOW(), NOW())'
    data = {
        'comment': comment,
        'user_id': session['id'],
        'message_id': message_id
    }
    mysql.query_db(query, data)
    return redirect('/wall')


@app.route('/delete/<comment_id>', methods=['POST'])
def delete(comment_id):
    query = 'SELECT created_at FROM comments where comments.id = :comment_id'
    data = {
        'comment_id': comment_id
    }
    date = mysql.query_db(query, data)
    created = date[0]['created_at']
    timesince = datetime.datetime.now() - created
    minutessince = int(timesince.total_seconds() / 60)
    if minutessince < 30:
        query = 'DELETE FROM comments where comments.id = :comment_id'
        mysql.query_db(query, data)
        return redirect('/wall')
    else:
        flash('Cannot delete comment if more than 30 minutes since posting',
              'Error:CommentDelete')
        return redirect('/wall') '''
