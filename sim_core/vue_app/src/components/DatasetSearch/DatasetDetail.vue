<template>
  <div>
    <p>
      <router-link to="/">
        <el-link type="primary" size="small">&lt; Back to search results</el-link>
      </router-link>
    </p>
    <div v-if="dataset">
      <el-row :gutter="18">
        <el-col :sm="8">
          <el-row type="flex" justify="center">
            <el-image :src="dataset.banner" fit="cover"></el-image>
          </el-row>
        </el-col>
        <el-col :sm="16">
          <h3 class="dataset-title">{{ dataset.name }}</h3>
          <p>{{ dataset.description }}</p>
          <div class="updated information">
            Updated on {{ updatedDate }}
          </div>
          <div class="information">
            <p>
              Organization: {{ dataset.organizationName }}<br>
              Owner: {{ dataset.ownerName }}<br>
            </p>
            <p v-if="dataset.contributors.length">
              Contributors: <span v-for="(contributor, i) in dataset.contributors" :key="contributor">{{ contributor }}{{ i === dataset.contributors.length-1 ? "." : ", "}}</span>
            </p>
          </div>
          <p>
            <dataset-stats :dataset="dataset" />
          </p>
          <div class="actions">
            <a v-if="dataset.study" :href="`${osparcUrl}/study/${dataset.study.uuid}`" target="_blank">
              <el-button type="warning">Run simulation</el-button>
            </a>
            <el-link type="warning" v-if="dataset.study" :href="`https://discover.blackfynn.com/datasets/${this.dataset.id}`" target="_blank">Get dataset</el-link>
            <el-link type="warning" v-if="dataset.study" href="https://docs.osparc.io" target="_blank">oSPARC Docs</el-link>
          </div>
        </el-col>
      </el-row>
      <el-row class="markdown">
        <el-col>
          <markdown :markdown="dataset.markdown" />
        </el-col>
      </el-row>
    </div>
    <div v-else>
      <p>Sorry, we couldn't retreive the dataset for the given id.</p>
    </div>
  </div>
</template>

<script>
import moment from 'moment';
import Markdown from '../Markdown/Markdown.vue';
import DatasetStats from './DatasetStats.vue';

export default {
  name: 'dataset-detail',
  props: ['dataset', 'isFetching'],
  data() {
    return {
      osparcUrl: dataPortal.osparcUrl // injected in index.html
    }
  },
  computed: {
    updatedDate() {
      return moment.utc(this.dataset.updatedAt).format('MMMM D, YYYY')
    }
  },
  components: {
    Markdown,
    DatasetStats
  }
}
</script>

<style lang="scss" scoped>
.dataset-title {
  @media screen and (max-width: 768px) {
    margin-top: 1em;
  }
}
.markdown {
  margin-top: 30px;
}
.information {
  color: #525252;
}
.updated {
  font-size: 0.9em;
}
.actions a {
  margin-right: 20px;
}
</style>
