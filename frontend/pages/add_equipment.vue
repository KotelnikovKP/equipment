<template>
    <div class="container">
        <div class="row">
            <div class="col-lg-12">

                <nav aria-label="breadcrumb" class="mt-4">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item"><nuxt-link to="/">Список оборудования</nuxt-link></li>
                        <li class="breadcrumb-item active" aria-current="page">Добавление оборудования</li>
                    </ol>
                </nav>

                <p class="lead">Заполните данные для добавления оборудования:</p>

                <form name="equipment_form" @submit.prevent="equipmentCreate">

                    <div class="row mt-3">
                        <div class="col-md-12">
                            <div class="md-form mb-0">
                                <label for="equipment_type_name">Тип</label>
                                <input type="text" id="equipment_type_name" class="form-control" placeholder="Тип"
                                    v-model="equipment_type_name" @input="onChange">
                            </div>
                            <ul class="list-group" name="equipment_type_list" v-show="isOpen">
                                <button class="list-group-item list-group-item-action"
                                    v-for="equipment_type in equipment_types" :key="equipment_type.id"
                                    @click.prevent="setResult(equipment_type.id, equipment_type.name)" tabindex="-1">
                                    {{ equipment_type.name }} (маска='{{ equipment_type.serial_number_mask }}')
                                </button>
                                <button class="list-group-item list-group-item-action" v-show="count_equipment_types == 0"
                                    :key="-1" tabindex="-1" disabled>
                                    Ничего не найдено
                                </button>
                                <button class="list-group-item list-group-item-action" v-show="count_equipment_types > 10"
                                    :key="-2" tabindex="-1" disabled>
                                    ...всего найдено {{ count_equipment_types }} типов
                                </button>
                            </ul>
                        </div>
                    </div>

                    <div class="row mt-3">
                        <div class="col-md-12" v-bind:class="{ 'fld-error': $v.serial_number.$error }">
                            <div class="md-form mb-0">
                                <label for="serial_number">Серийные номера</label>
                                <textarea type="text" id="serial_number" rows="5" class="form-control md-textarea"
                                    placeholder="Список серийных номеров, разделенных ',' (запятыми)"
                                    v-model="serial_number" @input="$v.serial_number.$touch()"></textarea>
                            </div>
                            <span class="msg-error" v-if="!$v.serial_number.required">
                                <small>Поле обязательно для заполнения</small>
                            </span>
                        </div>
                    </div>

                    <div class="row mt-3">
                        <div class="col-md-12" v-bind:class="{ 'fld-error': $v.description.$error }">
                            <div class="md-form">
                                <label for="description">Примечание</label>
                                <textarea type="text" id="description" rows="5" class="form-control md-textarea"
                                    placeholder="Примечание" v-model="description"
                                    @input="$v.description.$touch()"></textarea>
                            </div>
                            <span class="msg-error" v-if="!$v.description.maxLength">
                                <small>Должно быть не больше {{ $v.description.$params.maxLength.max }}
                                    символов.</small>
                            </span>
                        </div>
                    </div>

                    <div class="row mt-3">
                        <div class="col-md-12">
                            <div class="md-form">
                                <label for="err_msg" id="err_msg_lbl" class="fld-error-all"
                                    style="display: none">Ошибка</label>
                                <p class="lead fld-error-all" id="err_msg" style="display: none">Ошибка</p>
                            </div>
                        </div>
                    </div>

                    <div class="text-center text-md-left mt-3">
                        <button class="btn btn-primary" type="submit" :disabled="!isComplete">Добавить</button>
                    </div>

                </form>

            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import { required, maxLength } from 'vuelidate/lib/validators'

export default {
    data() {
        return {
            equipment_type_id: 0,
            equipment_type_name: '',
            original_equipment_type_name: '',
            serial_number: '',
            description: '',
            equipment_types: [],
            count_equipment_types: 0,
            isOpen: false,
        }
    },
    head() {
        return {
            title: "Добавление оборудования",
        }
    },
    methods: {
        async onChange() {
            try {
                let response = await this.$axios.get(`http://127.0.0.1:8000/api/equipment-type?q=${this.equipment_type_name}`);
                this.equipment_types = response.data.result;
                this.count_equipment_types = response.data.retExtInfo.count_items;
                this.isOpen = true;
            } catch ({ response }) {
                console.log(response);
            }
        },
        setResult(id, name) {
            this.equipment_type_id = id;
            this.equipment_type_name = name;
            this.original_equipment_type_name = name;
            this.isOpen = false;
        },
        handleClickOutside(event) {
            if (!this.$el.contains(event.target)) {
                this.isOpen = false;
                this.equipment_type_name = this.original_equipment_type_name;
            }
        },
        async equipmentCreate() {
            this.isOpen = false;
            this.equipment_type_name = this.original_equipment_type_name;
            const serial_numbers = this.serial_number.split(",")
            var equipments = [];
            for (let i = 0; i < serial_numbers.length; i += 1) {
                let sn = serial_numbers[i].trim();
                if (sn != "") {
                    equipments.push({ "equipment_type": this.equipment_type_id, "serial_number": sn, "description": this.description });
                }
            };
            try {
                let response = await this.$axios.post(`/api/equipment`, equipments);
                console.log(response);
                if (response.data.retExtInfo.failed == 0) {
                    this.$router.push("/");
                } else {
                    const err_lbl = document.getElementById("err_msg_lbl");
                    err_lbl.innerHTML = "При загрузке возникли ошибки:";
                    err_lbl.style.display = "";
                    const err = document.getElementById("err_msg");
                    let msg = `Получено - ${response.data.retExtInfo.failed}, успешно сохранено - ${response.data.retExtInfo.saved}, ошибок - ${response.data.retExtInfo.failed}<br>`
                    msg += `Ошибки:<br>`
                    let err_array = response.data.retExtInfo.errors
                    for (let i = 0; i < err_array.length; i += 1) {
                        let f = err_array[i].error.indexOf('"');
                        let l = err_array[i].error.lastIndexOf('"');
                        msg += `${err_array[i].index}. <strong>${JSON.parse(err_array[i].data.replaceAll("'", '"')).serial_number}</strong>: ${err_array[i].error.substring(f + 1, l)}<br>`
                    }
                    err.innerHTML = msg;
                    err.style.display = "";
                }
            } catch ({ response }) {
                console.log(response);
                const err = document.getElementById("err_msg");
                err.innerHTML = JSON.stringify(response.data);
                err.style.display = "";
                const err_lbl = document.getElementById("err_msg_lbl");
                err_lbl.innerHTML = "Error " + response.status + " (" + response.statusText + "):"
                err_lbl.style.display = "";
            }
        },
    },
    mounted() {
        document.addEventListener('click', this.handleClickOutside);
    },
    destroyed() {
        document.removeEventListener('click', this.handleClickOutside);
    },
    computed: {
        isComplete() {
            return !this.$v.$invalid && this.equipment_type_id != 0;
        }
    },
    validations: {
        serial_number: {
            required,
        },
        description: {
            maxLength: maxLength(40960)
        },
    },
}
</script>

<style type="text/css">
.fld-error-all {
    display: block;
    color: #dc3545;
}

.fld-error .msg-error {
    display: block;
    color: #dc3545;
}

.msg-error {
    display: none;
}
</style>