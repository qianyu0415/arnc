<template>
  <div class="video-generator">
    <base-header class="pb-6 pb-8 pt-5 pt-md-8 bg-gradient-success">
      <b-row>
        <b-col xl="12" md="6">
          <stats-card title="En3D"
                      type="gradient-red"
                      sub-title="库里、梅西穿越到古画是一种什么体验，快来试试吧！"
                      icon="ni ni-active-40"
                      class="mb-4">
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
                <b-form-input id="charac_id" v-model="charac_id" placeholder="请输入人物ID" class="mb-2"></b-form-input>
                <label for="charac_id" class="form-label">人物ID:</label>
              </div>
              <div class="form-group">
                <b-form-input id="action_id" v-model="action_id" placeholder="请输入动作ID" class="mb-2"></b-form-input>
                <label for="action_id" class="form-label">动作ID:</label>
              </div>
              <!-- ThreeScene Component -->
              <three-scene @camera-info-updated="handleCameraInfoUpdated"></three-scene>
              <div v-if="cameraInfo">
                <h3>Camera Position and Rotation</h3>
                <b-form>
                  <b-form-group label="Position X:" v-model="cameraInfo.position.x">
                    <b-form-input readonly :value="cameraInfo.position.x"></b-form-input>
                  </b-form-group>
                  <b-form-group label="Position Y:" v-model="cameraInfo.position.y">
                    <b-form-input readonly :value="cameraInfo.position.y"></b-form-input>
                  </b-form-group>
                  <b-form-group label="Position Z:" v-model="cameraInfo.position.z">
                    <b-form-input readonly :value="cameraInfo.position.z"></b-form-input>
                  </b-form-group>
                  <b-form-group label="Rotation X (Degrees):" v-model="cameraInfo.rotation.x">
                    <b-form-input readonly :value="cameraInfo.rotation.x"></b-form-input>
                  </b-form-group>
                  <b-form-group label="Rotation Y (Degrees):" v-model="cameraInfo.rotation.y">
                    <b-form-input readonly :value="cameraInfo.rotation.y"></b-form-input>
                  </b-form-group>
                  <b-form-group label="Rotation Z (Degrees):" v-model="cameraInfo.rotation.z">
                    <b-form-input readonly :value="cameraInfo.rotation.z"></b-form-input>
                  </b-form-group>
                </b-form>
              </div>
              <b-button type="submit" variant="primary" class="submit-btn">生成视频</b-button>
            </b-form>
          </b-card>
        </b-col>
      </b-row>
      <!-- Video Preview -->
      <b-row v-if="videoUrl">
        <b-col md="12" class="mt-3">
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
import ThreeScene from './ThreeScene.vue';

export default {
  components: {
    ThreeScene,
  },
  data() {
    return {
      charac_id: '',
      action_id: '',
      videoUrl: null,
      cameraInfo: {
        position: { x: '', y: '', z: '' },
        rotation: { x: '', y: '', z: '' }
      },
    };
  },
  methods: {
    submitForm() {
      const formData = new FormData();
      formData.append('charac_id', this.charac_id);
      formData.append('action_id', this.action_id);

      axios.post('https://u349276-86a4-e5e4bb69.westb.seetacloud.com:8443/generate-3D-video', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        responseType: 'blob'
      })
      .then(response => {
        this.videoUrl = URL.createObjectURL(new Blob([response.data], { type: 'video/mp4' }));
      })
      .catch(error => console.error('Error:', error));
    },
    handleCameraInfoUpdated(info) {
      this.cameraInfo = info;
    },
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
  width: 100%;
  padding-top: 56.25%;
}
.video-preview video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
