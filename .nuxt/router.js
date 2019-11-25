import Vue from 'vue'
import Router from 'vue-router'
import { interopDefault } from './utils'
import scrollBehavior from './router.scrollBehavior.js'

const _734c46df = () => interopDefault(import('../pages/about/index.vue' /* webpackChunkName: "pages/about/index" */))
const _30bc5224 = () => interopDefault(import('../pages/data/index.vue' /* webpackChunkName: "pages/data/index" */))
const _c203f452 = () => interopDefault(import('../pages/datasets/_datasetId.vue' /* webpackChunkName: "pages/datasets/_datasetId" */))
const _08b61021 = () => interopDefault(import('../pages/index.vue' /* webpackChunkName: "pages/index" */))

Vue.use(Router)

export const routerOptions = {
  mode: 'history',
  base: decodeURI('/'),
  linkActiveClass: 'nuxt-link-active',
  linkExactActiveClass: 'nuxt-link-exact-active',
  scrollBehavior,

  routes: [{
    path: "/about",
    component: _734c46df,
    name: "about"
  }, {
    path: "/data",
    component: _30bc5224,
    name: "data"
  }, {
    path: "/datasets/:datasetId?",
    component: _c203f452,
    name: "datasets-datasetId"
  }, {
    path: "/",
    component: _08b61021,
    name: "index"
  }],

  fallback: false
}

export function createRouter () {
  return new Router(routerOptions)
}
