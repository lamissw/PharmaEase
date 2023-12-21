import 'package:pharmaease/src/model/location_model.dart';
import 'package:pharmaease/src/model/medicine_model.dart';
import 'package:pharmaease/src/model/pharmacist_model.dart';
import 'package:json_annotation/json_annotation.dart';

part 'pharmacy_details_model.g.dart';

@JsonSerializable()
class PharmacyDetailsModel {
  final String id;
  final String name;
  final String email;
  final String description;
  // final String pharmacyImage;
  // final String pharmacyArea;
  // final String pharmacyDistance;
  // final DateTime pharmacyOpeningHours;
  // final DateTime pharmacyClosingHours;
  // final String pharmacyPhoneNumber;
  final LocationModel location;
  final List<DrugModel> drugs;
  final List<PharmacistModel> pharmacists;

  PharmacyDetailsModel({
    required this.id,
    required this.name,
    required this.email,
    required this.description,
    // required this.pharmacyImage,
    // required this.pharmacyArea,
    // required this.pharmacyDistance,
    // required this.pharmacyOpeningHours,
    // required this.pharmacyClosingHours,
    // required this.pharmacyPhoneNumber,
    required this.location,
    required this.drugs,
    required this.pharmacists,
  });

  factory PharmacyDetailsModel.fromJson(Map<String, dynamic> json) {
    return _$PharmacyDetailsModelFromJson(json);
  }

  Map<String, dynamic> toJson() => _$PharmacyDetailsModelToJson(this);
}
