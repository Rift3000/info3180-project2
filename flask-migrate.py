from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app # we import the app object from the app module
from app import db

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()




"""const Upload = Vue.component('upload-form', {
    template: `

    <div class="container">
    /*<alert v-show="messages"></alert>
    <error /*v-show="mess"> </error>*/
    <h2>Upload your Photo</h2>
    <form @submit.prevent="uploadPhoto"  id="uploadForm" method="post" enctype="multipart/form-data">
        <div class="form-group">
            <label> Description: </label><br/>
            <textarea name="description" rows="5" cols="55">
            </textarea>

            <label> Photo: </label>
            <input type="file" name="photo" placeholder="choose an image" />
        </div>

        <button name="submit" class="btn btn-primary">Upload</button>
    </form>
    </div>
    `,

    data() {
        return {
            messages: false,
            mess: true,
        };
    },


    methods: {

        uploadPhoto: function() {
        let self = this;
        let uploadForm = document.getElementById('uploadForm');
        let form_data = new FormData(uploadForm);

        fetch("/api/upload", {
                method: 'POST',
                body: form_data,
                headers: {
                    'X-CSRFToken': token
                },
                credentials: 'same-origin'
        })
                .then(function (response) {
                    return response.json();
        })
                .then(function (jsonResponse) {
            // display a success message
                    console.log(jsonResponse);
        })
            .catch(function (error) {
            console.log(error);
        });

        }
    }

});"""