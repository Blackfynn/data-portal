import Vue from 'vue'
import Router from 'vue-router'
import { interopDefault } from './utils'
import scrollBehavior from './router.scrollBehavior.js'

const _0ccbd8d9 = () => interopDefault(import('../pages/about/index.vue' /* webpackChunkName: "pages/about/index" */))
const _7969c498 = () => interopDefault(import('../pages/data/index.vue' /* webpackChunkName: "pages/data/index" */))
const _519e045e = () => interopDefault(import('../pages/datasets/_datasetId.vue' /* webpackChunkName: "pages/datasets/_datasetId" */))
const _55e1259b = () => interopDefault(import('../pages/index.vue' /* webpackChunkName: "pages/index" */))

Vue.use(Router)

export const routerOptions = {
  mode: 'history',
  base: decodeURI('/'),
  linkActiveClass: 'nuxt-link-active',
  linkExactActiveClass: 'nuxt-link-exact-active',
  scrollBehavior,

  routes: [{
    path: "/about",
    component: _0ccbd8d9,
    name: "about"
  }, {
    path: "/data",
    component: _7969c498,
    name: "data"
  }, {
    path: "/datasets/:datasetId?",
    component: _519e045e,
    name: "datasets-datasetId"
  }, {
    path: "/",
    component: _55e1259b,
    name: "index"
  }],

  fallback: false
}

export function createRouter () {
  return new Router(routerOptions)
}
