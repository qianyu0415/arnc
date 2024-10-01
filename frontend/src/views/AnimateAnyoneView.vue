<template>
    <div class="video-generator">
      <base-header class="pb-6 pb-8 pt-5 pt-md-8 bg-gradient-success">
        <!-- Card stats -->
      <b-row>
          <b-col xl="12" md="6">
            <stats-card title="AnimateAnyone"
                        type="gradient-red"
                        sub-title="AI动画新境界，快来让你喜欢的人物动起来吧！"
                        icon="ni ni-active-40"
                        class="mb-4">
              <template v-slot:footer>
              </template>
            </stats-card>
          </b-col>
        </b-row>
      </base-header>
      <b-container fluid class="mt--7">
        <b-row>
          <b-col md="12">
            <b-card>
              <b-form @submit.prevent="submitForm" class="text-center">
                <div class="form-group">
                  <b-form-input id="imagePath" v-model="imagePath" placeholder="Enter image path" class="mb-2"></b-form-input>
                  <label for="imagePath" class="form-label">Reference Image Path:</label>
                </div>
                <div class="form-group">
                  <b-form-input id="posePath" v-model="posePath" placeholder="Enter pose video path" class="mb-2"></b-form-input>
                  <label for="posePath" class="form-label">Pose Video Path:</label>
                </div>
                <b-button type="submit" variant="primary" class="submit-btn">Generate Video</b-button>
              </b-form>
            </b-card>
          </b-col>
        </b-row>
        <b-row>
          <b-col md="12" class="mt-3" v-if="videoUrl">
            <b-card>
              <h3 class="text-center">Generated Video:</h3>
              <div class="video-preview">
                <video controls class="w-100">
                  <source :src="videoUrl" type="video/mp4">
                  Your browser does not support the video tag.
                </video>
              </div>
            </b-card>
          </b-col>
        </b-row>
      </b-container>
    </div>
  </template>
<script>
import axios from 'axios';

export default {
  data() {
    return {
      imagePath: '',
      posePath: '',
      videoUrl: null
    };
  },
  methods: {
    submitForm() {
      const formData = new FormData();
      formData.append('path_img', this.imagePath);
      formData.append('path_pose', this.posePath);

      axios.post(`${process.env.VUE_APP_API_URL}/animate`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        responseType: 'blob' // Assuming the response is a video file
      })
      .then(response => {
        // Create a URL for the blob response for video display
        const url = URL.createObjectURL(new Blob([response.data], { type: 'video/mp4' }));
        this.videoUrl = url;
      })
      .catch(error => console.error('Error:', error));
    }
  }
};
</script>
<style scoped>
.video-generator {
  text-align: center;
}

.form-group {
  margin-bottom: 20px;
}

.input-field, .submit-btn {
  margin: 10px 0;
  padding: 10px;
  border-radius: 4px;
  width: 80%;
  margin-left: auto;
  margin-right: auto;
}

.submit-btn {
  background-color: #559dfa;
  color: white;
  border: none;
  cursor: pointer;
}

.submit-btn:hover {
  background-color: #1057c9;
}

.video-preview {
  position: relative;
  width: 100%; /* Adjust width as necessary */
  padding-top: 56.25%; /* 16:9 Aspect Ratio */
}

.video-preview video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
