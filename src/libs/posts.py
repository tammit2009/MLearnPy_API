from flask import request, render_template, redirect

from src.libs.database import BlogPost, db

def posts_register(app):

    @app.route('/posts', methods=['POST', 'GET'])
    def posts():
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)

    @app.route('/posts/new', methods=['GET', 'POST'])   
    def new_post():
        if request.method == 'POST':
            # extract the data
            post_title = request.form['title']
            post_content = request.form['content']
            post_author = request.form['author']

            # create the post object
            new_post = BlogPost(title=post_title, content=post_content, author=post_author)

            # save and commit the new post object
            db.session.add(new_post)
            db.session.commit()

            return redirect('/posts')
        else:
            return render_template('new_post.html')

    @app.route('/posts/delete/<int:id>')
    def delete_post(id):
        post = BlogPost.query.get_or_404(id)
        db.session.delete(post)
        db.session.commit()
        return redirect('/posts')

    @app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
    def edit_post(id):
        post = BlogPost.query.get_or_404(id)

        if request.method == 'POST':
            # extract the data
            post.title = request.form['title']
            post.content = request.form['content']
            post.author = request.form['author']
            db.session.commit()
            return redirect('/posts')
        else: 
            return render_template('edit_post.html', post=post)
