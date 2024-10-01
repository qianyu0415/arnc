import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    // 其他状态
    processedFileName: '', // 用于存储文件名的状态
    processedImageURL:'',
  },
  mutations: {
    // 其他mutations
    SET_PROCESSED_FILE_NAME(state, fileName) {
      state.processedFileName = fileName;
    },
    // 添加 mutation 来更新图片 URL
    SET_PROCESSED_IMAGE_URL(state, url) {
      state.processedImageURL = url;
    }
  },
  actions: {
    // 其他actions
    setProcessedFileName({ commit }, fileName) {
      commit('SET_PROCESSED_FILE_NAME', fileName);
    },
    setProcessedImageURL({ commit }, url) {
      commit('SET_PROCESSED_IMAGE_URL', url);
    }
  },
  
});

  
