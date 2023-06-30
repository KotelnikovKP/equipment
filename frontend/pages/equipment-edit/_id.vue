<template>
    <div class="container">
        <div class="row">
            <div class="col-lg-12">

                <nav aria-label="breadcrumb" class="mt-4">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item"><nuxt-link to="/">Список оборудования</nuxt-link></li>
                        <li class="breadcrumb-item active" aria-current="page">{{ id }}</li>
                    </ol>
                </nav>

                <p class="lead">Внесите изменения в данные оборудования:</p>

                <form name="equipment_form" @submit.prevent="equipmentUpdate">

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
                                <label for="serial_number">Серийный номер</label>
                                <input type="text" id="serial_number" class="form-control" placeholder="Серийный номер"
                                    v-model="serial_number" @input="$v.serial_number.$touch()">
                            </div>
                            <span class="msg-error" v-if="!$v.serial_number.required">
                                <small>Поле обязательно для заполнения</small>
                            </span>
                            <span class="msg-error" v-if="!$v.serial_number.maxLength">
                                <small>Должно быть не больше {{ $v.serial_number.$params.maxLength.max }}
                                    символов.</small>
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
                        <button class="btn btn-primary" type="submit" :disabled="$v.$invalid">Обновить</button>
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
            id: 0,
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
    async asyncData({ params }) {
        return {
            id: params.id,
        }
    },
    head() {
        return {
            title: "Изменение оборудования " + this.equipment_type_name + " s/n " + this.serial_number,
        }
    },
    methods: {
        async getEquipment() {
            try {
                let equipment = await this.$axios.get(`http://127.0.0.1:8000/api/equipment/${this.id}`);
                this.id = equipment.data.result.id;
                this.equipment_type_id = equipment.data.result.equipment_type;
                this.equipment_type_name = equipment.data.result.equipment_type_name;
                this.original_equipment_type_name = equipment.data.result.equipment_type_name;
                this.serial_number = equipment.data.result.serial_number;
                this.description = equipment.data.result.description;
            } catch ({ response }) {
                console.log(response);
            }
        },
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
        async equipmentUpdate() {
            try {
                this.isOpen = false;
                this.equipment_type_name = this.original_equipment_type_name;
                let response = await this.$axios.put(`/api/equipment/${this.id}`, {
                    equipment_type: this.equipment_type_id,
                    serial_number: this.serial_number,
                    description: this.description
                })
                this.$router.back()
                // this.$router.push("/");
            } catch ({ response }) {
                console.log(response);
                const err = document.getElementById("err_msg");
                err.innerHTML = JSON.stringify(response.data.non_field_errors[0]);
                err.style.display = "";
                const err_lbl = document.getElementById("err_msg_lbl");
                err_lbl.innerHTML = "При загрузке возникла ошибка:"
                err_lbl.style.display = "";
            }

        },
    },
    mounted() {
        this.getEquipment();
        document.addEventListener('click', this.handleClickOutside);
    },
    destroyed() {
        document.removeEventListener('click', this.handleClickOutside);
    },
    validations: {
        serial_number: {
            required,
            maxLength: maxLength(50)
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