namespace Petshop.Models
{
    public class Animal
    {
        //REQUIRED
        public int Id { get; set; }
        public string Nome { get; set; }
        public string Especie { get; set; }
        public string Raca { get; set; }
        public int Idade { get; set; }
        public int ClienteId { get; set; }         // animal pertence a um cliente (obrigatório)
        public int? PlanoId { get; set; }          // plano pode ser opcional para um animal
        public Cliente? Dono { get; set; }
        public Plano? PlanoAnimal { get; set; }
    }
}