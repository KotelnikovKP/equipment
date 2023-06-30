<template>
    <div class="container">
        <h1 class="my-3">Список оборудования</h1>
        <div v-if="loggedIn">
            <div class="row mt-3">
                <div class="col-md-12">
                    <div class="md-form mb-2">
                        <form class="input-group search-form">
                            <input type="text" class="form-control" name="q" placeholder="Поиск по списку оборудования"
                                v-model="q">
                            <span class="input-group-btn ml-2">
                                <button class="btn btn-secondary" @click.stop.prevent="fetchPage(1)"> Найти </button>
                            </span>
                        </form>
                    </div>
                </div>
            </div>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th scope="col">id</th>
                        <th scope="col">Тип</th>
                        <th scope="col">Серийный номер</th>
                        <th scope="col">Примечание</th>
                        <th scope="col" colspan="2">Действия</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="equipment in equipments" :key="equipment.id">
                        <td>{{ equipment.id }}</td>
                        <td>{{ equipment.equipment_type_name }}</td>
                        <td>{{ equipment.serial_number }}</td>
                        <td class="truncate">{{ equipment.description }}</td>
                        <td width="1rem" data="Изменить" title="Изменить">
                            <nuxt-link :to="`/equipment-edit/${equipment.id}`" class="btn btn-sm btn-outline-secondary">
                                <img src="/images/edit.png" class="image-table" alt="edit">
                            </nuxt-link>
                        </td>
                        <td width="1rem" data="Удалить" title="Удалить">
                            <nuxt-link :to="`/equipment-delete/${equipment.id}`" class="btn btn-sm btn-outline-secondary">
                                <img src="/images/delete.png" class="image-table" alt="delete">
                            </nuxt-link>
                        </td>
                    </tr>
                </tbody>
            </table>
            <nav aria-label="Paginate me">
                <ul class="pagination justify-content-center" ref="nav">
                    <button v-if="previous_page != null" class="page-link" @click="fetchPage(previous_page);"
                        tabindex="-1">Предыдущая</button>
                    <li v-else class="page-item disabled">
                        <a class="page-link disabled" href="#" tabindex="-1">Предыдущая</a>
                    </li>
                    <li v-if="current_page > 3" class="page-item ml-2 disabled">
                        <button class="page-link" style="border: 0">...</button>
                    </li>
                    <span v-for="i in page_count">
                        <li v-if="current_page === i" class="page-item ml-2 active">
                            <button class="page-link">{{ i }}</button>
                        </li>
                        <li v-else-if="(i >= current_page - 2) && (i <= current_page + 2)" class="page-item ml-2">
                            <button class="page-link" @click="fetchPage(i);">{{ i }}</button>
                        </li>
                    </span>
                    <li v-if="current_page < page_count - 2" class="page-item ml-2 disabled">
                        <button class="page-link" style="border: 0">...</button>
                    </li>
                    <button v-if="next_page != null" class="page-link ml-2"
                        @click="fetchPage(next_page);">Следующая</button>
                    <li v-else class="page-item ml-2 disabled">
                        <a class="page-link" href="#">Следующая</a>
                    </li>
                </ul>
            </nav>
            <div class="row mt-3">
                <div class="col-md-12">
                    <p class="lead">Найдено записей: {{ count_items }}</p>
                </div>
            </div>
        </div>
        <div v-else>
            <h6 class="card-header"><nuxt-link to="/signin">Авторизуйтесь</nuxt-link> или <nuxt-link
                    to="/signup">зарегистрируйтесь</nuxt-link> для получения доступа к списку оборудования</h6>
        </div>
    </div>
</template>

<script>
import axios from "axios";
export default {
    data() {
        return {
            equipments: [],
            count_items: 0,
            items_per_page: 0,
            start_item_index: 0,
            end_item_index: 0,
            previous_page: null,
            current_page: 1,
            next_page: null,
            page_count: 0,
            q: '',
        }
    },
    head() {
        return {
            title: "Список оборудования",
        }
    }, 
    methods: {
        async fetchPage(p) {
            if (this.loggedIn) {
                try {
                    let response = await this.$axios.get(`http://127.0.0.1:8000/api/equipment?q=${this.q}&page=${p}`);
                    this.equipments = response.data.result;
                    this.count_items = response.data.retExtInfo.count_items;
                    this.items_per_page = response.data.retExtInfo.items_per_page;
                    this.start_item_index = response.data.retExtInfo.start_item_index;
                    this.end_item_index = response.data.retExtInfo.end_item_index;
                    this.previous_page = response.data.retExtInfo.previous_page;
                    this.current_page = response.data.retExtInfo.current_page;
                    this.next_page = response.data.retExtInfo.next_page;
                    this.page_count = Math.ceil(response.data.retExtInfo.count_items / response.data.retExtInfo.items_per_page);
                } catch ({ response }) {
                    console.log(response);
                }
            }
        },
    },
    mounted() {
        this.fetchPage(1);
    },
    computed: {
        loggedIn() {
            return this.$auth.loggedIn
        },
        user() {
            return this.$auth.user
        },
        token() {
            return this.$auth.strategy.token.get()
        }
    }
}
</script>

<style type="text/css"></style>
