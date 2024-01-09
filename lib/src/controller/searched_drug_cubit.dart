
import 'package:bloc/bloc.dart';
import 'package:dio/dio.dart';
import 'package:get_it/get_it.dart';
import 'package:pharmaease_api/pharmaease_api.dart';
import 'package:built_collection/built_collection.dart';

class SearchedDrugCubit extends Cubit<SearchedDrugState> {
  SearchedDrugCubit() : super(InitialSearchedDrugState()) {}
  final PharmaeaseApi _api = GetIt.I.get<PharmaeaseApi>();

  List<Drug>? drugs=[];
  // Drug ?drug;


  Future<dynamic> getSearchedDrug(String drugName) async {
    try {
      emit(LoadingSearchedDrugState());
      List<Drug>? result = (await _api
          .getDrugApi()
          .getDrugByNameOrBarcodeApiDrugDrugGet(drugName: "panadol"))
          .data!.toList();

      print("AHHHHHHHH");
      print(result);
      if (result == null) {
        emit(ErrorSearchedDrugState());
      } else {
        drugs = result;
        emit(LoadedSearchedDrugState(drugs));
      }
    } on DioException catch (e) {
      if (e.response!.statusCode == 401) {
        emit(ErrorSearchedDrugState());
        print("Errorrrrr: $e");
        throw Exception("Drug not found");
      }
      print("ERRORRR $e");
    }
  }
}

abstract class SearchedDrugState {}

class InitialSearchedDrugState extends SearchedDrugState {}

class LoadingSearchedDrugState extends SearchedDrugState {}

class LoadedSearchedDrugState extends SearchedDrugState {
  final List<Drug> ?drugs;
  LoadedSearchedDrugState(this.drugs);
}

class ErrorSearchedDrugState extends SearchedDrugState {}