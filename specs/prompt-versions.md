# Assuming existing code structure with necessary imports and configurations
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prompts.db'
db = SQLAlchemy(app)

# Assume existing Prompt model present
class Prompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

# New Version model based on the requirement
class Version(db.Model):
    version_id = db.Column(db.Integer, primary_key=True)
    prompt_id = db.Column(db.Integer, db.ForeignKey('prompt.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_by = db.Column(db.String(100), nullable=False)

# API Endpoint to list all versions of a prompt
@app.route('/prompts/<int:prompt_id>/versions', methods=['GET'])
def get_versions(prompt_id):
    versions = Version.query.filter_by(prompt_id=prompt_id).all()
    return jsonify([
        {
            'version_id': version.version_id,
            'content': version.content,
            'created_at': version.created_at,
            'created_by': version.created_by
        }
        for version in versions
    ])

# API Endpoint to revert a prompt to a specific version
@app.route('/prompts/<int:prompt_id>/revert/<int:version_id>', methods=['PATCH'])
def revert_to_version(prompt_id, version_id):
    version = Version.query.filter_by(prompt_id=prompt_id, version_id=version_id).first()
    if not version:
        return jsonify({'error': 'Version not found'}), 404

    # Create new version to store the current state before reverting
    new_version = Version(prompt_id=prompt_id, content=version.content, created_by='system')  # Assuming 'system' does the reverting
    db.session.add(new_version)
    db.session.commit()

    return jsonify({
        'version_id': new_version.version_id,
        'content': new_version.content,
        'created_at': new_version.created_at,
        'created_by': new_version.created_by
    })

# Edge Case: Pagination (if needed in future)
def get_paginated_versions(prompt_id, page=1, per_page=10):
    paginated_versions = Version.query.filter_by(prompt_id=prompt_id).paginate(page, per_page, error_out=False)
    return jsonify({
        'versions': [
            {
                'version_id': version.version_id,
                'content': version.content,
                'created_at': version.created_at,
                'created_by': version.created_by
            }
            for version in paginated_versions.items
        ],
        'total_pages': paginated_versions.pages,
        'current_page': page
    })

# To run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

