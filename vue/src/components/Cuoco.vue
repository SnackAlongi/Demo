<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Ricette</h1>
        <hr><br><br>
        <form>
          Ricetta:<br>
          <input type="text" name="Ricetta">
          <br>
          Procedimento:<br>
          <input type="text" name="Procedimento">
        </form>
        <button type="button" class="btn btn-success btn-sm">Aggiungi Ricetta</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Ricetta</th>
              <th scope="col">Procedimento</th>
              <th scope="col">Modifica</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(ricetta, index) in ricette" :key="index">
              <td>{{ ricetta.NomeRicetta }}</td>
              <td>{{ ricetta.Procedimento }}</td>
              <td>
                <button type="button" class="btn btn-warning btn-sm">Update</button>
                <button type="button" class="btn btn-danger btn-sm">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios';


export default {
  data() {
    return {
      ricette: [],
      aggiungiRicettaForm: {
        NomeRicetta: ricetta,
        Procedimento: 'fare la cotoletta',
      },
    };
  },
  methods: {
    getRicette() {
      const path = 'http://localhost:5000/ricetta';
      axios.get(path)
        .then((res) => {
          this.ricette = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    insertRicette() {
      const path = 'http://localhost:5000/ricetta';
      axios.post(path, payload)
        .then(() => {
          this.getBooks();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getRicette();
        });
    },
  },
  created() {
    this.getRicette();
  },
};

</script>
