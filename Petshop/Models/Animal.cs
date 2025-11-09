using System.ComponentModel.DataAnnotations;
namespace Petshop.Models
{
    public class Animal
    {
        public int Id { get; set; }
        [Required(ErrorMessage ="É necessário preencher o nome")]
        public string Nome { get; set; }
        [Required(ErrorMessage ="É necessário preencher a especie")]
        [RegularExpression("^(Cachorro|Gato)$", ErrorMessage = "Espécie deve ser apenas Cachorro ou Gato.")]
        public string Especie { get; set; }
        public string Raca { get; set; }
        public int Idade { get; set; }
        public int ClienteId { get; set; }         
        public int? PlanoId { get; set; }          // plano pode ser opcional para um animal
        public Cliente? Dono { get; set; }
        public Plano? PlanoAnimal { get; set; }
    }
}