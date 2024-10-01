<template>
  <div>
    <base-header class="pb-6 pb-8 pt-5 pt-md-8 bg-gradient-success">
      <!-- Card stats and upload form inside header -->
      <b-row>
        <b-col xl="12" md="6">
          <stats-card title="Inpainting"
                      type="gradient-red"
                      sub-title="如果不想选坐标，不如试试这个功能，自动去除(人物效果更好哦)"
                      icon="ni ni-active-40"
                      class="mb-4">
            <!-- This slot is left empty for now -->
          </stats-card>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12">
          <div class="text-center">
            <h2 class="text-white">Image Upload & Processing</h2>
            <b-form @submit.prevent="submitForm">
              <b-form-file v-model="selectedFile" @change="handleFileUpload" class="mb-2 text-center"></b-form-file>
              <b-form-input v-model="dilateKernelSize" placeholder="膨胀核大小" class="mb-2 text-center"></b-form-input>
              <!-- 如果有其他参数，继续在这里添加输入框 -->
              <b-button type="submit" variant="primary">处理图片</b-button>
            </b-form>
          </div>
        </b-col>
      </b-row>
    </base-header>
    <b-container fluid class="image-uploader mt-4">
      <b-row>
        <b-col md="6" class="mt-3" v-if="uploadedImageUrl">
          <b-card>
            <div class="image-preview">
              <b-card-img :src="uploadedImageUrl" alt="Uploaded Image"></b-card-img>
            </div>
            <b-card-footer>
              <small class="text-muted">Original Image</small>
            </b-card-footer>
          </b-card>
        </b-col>
        <b-col md="6" class="mt-3" v-if="processedImageUrl">
          <b-card>
            <div class="processed-image">
              <b-card-img :src="processedImageUrl" alt="Processed Image"></b-card-img>
            </div>
            <b-card-footer class="text-muted">
              <small class="text-muted">Processed Image</small>
            </b-card-footer>
          </b-card>
        </b-col>
      </b-row>
      <b-row v-if="errorMessage">
        <b-col>
          <b-alert variant="danger" show>{{ errorMessage }}</b-alert>
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
      selectedFile: null,
      dilateKernelSize: 15, // 示例参数，根据实际情况调整
      // 在这里初始化其他参数
      uploadedImageUrl: null,
      processedImageUrl: null,
      errorMessage: null, // 用于存储和显示错误信息
    };
  },
  methods: {
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
      if (this.selectedFile) {
        this.uploadedImageUrl = URL.createObjectURL(this.selectedFile);
        this.errorMessage = null; // 重置错误信息
      }
    },
    async submitForm() {
      if (!this.selectedFile) {
        this.errorMessage = '请先选择一个文件。';
        return;
      }
      
      const formData = new FormData();
      formData.append('input_img', this.selectedFile);
      formData.append('dilate_kernel_size', this.dilateKernelSize);
      // 将其他参数添加到 formData
      
      // 从localStorage获取JWT
      const token = localStorage.getItem('userToken');
      console.log('Token:', token);

      try {
        const response = await axios.post(`${process.env.VUE_APP_API_URL}/inpainting_automatically`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            // 在请求头中附带JWT
            'Authorization': `Bearer ${token}`
          },
          responseType: 'blob', // 通知axios以blob形式接收响应体
        });
        
        // 创建一个从Blob对象生成的URL，并将其设置为图片的src
        const url = URL.createObjectURL(new Blob([response.data]));
        this.processedImageUrl = url; // 使用创建的URL
        this.errorMessage = null; // 成功后重置错误信息
      } catch (error) {
        console.error(error);
        this.errorMessage = error.response && error.response.data ? error.response.data.error : '处理图片时发生未知错误。';
        this.processedImageUrl = null; // 出错时重置处理后的图片 URL
      }
    },
  },
};
</script>

<style scoped>
.image-uploader {
  text-align: center;
}

.image-preview img, .processed-image img {
  max-width: 100%;
  height: auto;
}
</style>
