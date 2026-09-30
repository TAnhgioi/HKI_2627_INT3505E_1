from flask import Flask, jsonify, request

app = Flask(__name__)

posts = [
    {
        "id": 1,
        "title": "Bài viết đầu tiên",
        "content": "Nội dung bài viết mẫu",
        "author_id": 101
    },
    {
        "id": 2,
        "title": "Tìm hiểu RESTful API",
        "content": "Kiến trúc thiết kế API tiêu chuẩn",
        "author_id": 102
    }
]

# 1. GET /api/v1/posts - Lấy danh sách tất cả bài viết
@app.route('/api/v1/posts', methods=['GET'])
def get_posts():
    return jsonify({
        "status": "success",
        "data": posts,
        "total": len(posts)
    }), 200

# 2. POST /api/v1/posts - Tạo bài viết mới
@app.route('/api/v1/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({
            "status": "error",
            "message": "Tiêu đề (title) và nội dung (content) là bắt buộc."
        }), 400

    new_post = {
        "id": len(posts) + 1,
        "title": data['title'],
        "content": data['content'],
        "author_id": data.get('author_id', 1)
    }
    posts.append(new_post)
    
    return jsonify({
        "status": "success",
        "message": "Tạo bài viết thành công",
        "data": new_post
    }), 201

# 3. GET /api/v1/posts/<int:post_id> - Lấy thông tin chi tiết 1 bài viết
@app.route('/api/v1/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        return jsonify({"status": "error", "message": "Không tìm thấy bài viết"}), 404
    
    return jsonify({"status": "success", "data": post}), 200

# 4. PUT /api/v1/posts/<int:post_id> - Cập nhật bài viết
@app.route('/api/v1/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        return jsonify({"status": "error", "message": "Không tìm thấy bài viết"}), 404
    
    data = request.get_json()
    post['title'] = data.get('title', post['title'])
    post['content'] = data.get('content', post['content'])
    
    return jsonify({
        "status": "success",
        "message": "Cập nhật thành công",
        "data": post
    }), 200

# 5. DELETE /api/v1/posts/<int:post_id> - Xóa bài viết
@app.route('/api/v1/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global posts
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        return jsonify({"status": "error", "message": "Không tìm thấy bài viết"}), 404
    
    posts = [p for p in posts if p["id"] != post_id]
    return jsonify({
        "status": "success",
        "message": f"Đã xóa bài viết có ID {post_id}"
    }), 200

if __name__ == '__main__':
    app.run(debug=True)